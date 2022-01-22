from Project import Project
import logging
import sys
import sqlite3
from sqlite3 import Error
import shutil 
import os

logging.basicConfig(filename='duplicates.log', filemode='a',
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by the db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

def get_project_id(conn):
	sql = "select id from (select id from GitHub_Projects union select id from MATC_Projects) order by id"
	cur = conn.cursor()
	cur.execute(sql)

	rows = cur.fetchall()
	return [r[0] for r in rows]


def get_github_project_id(conn):
	sql = "select id from GitHub_Projects order by id"
	cur = conn.cursor()
	cur.execute(sql)

	rows = cur.fetchall()
	return [r[0] for r in rows]

def isduplicate(p1,p2):
	if len(p1.model_files)!= len(p2.model_files) or len(p2.model_files) ==0 or len(p1.model_files)==0:
		return False
	p1_models = p1.model_files
	p2_models = p2.model_files  
	common = []
	for i in range(0, len(p1_models)):
		ith_model = p1_models[i]
		for j in range(0, len(p2_models)):
			if ith_model == p2_models[j]:
				common.append(i)
				break
	
	if len(common)==len(p1_models):
		return True
	return False

def get_duplicate_projects(project_objs):
	duplicate_projects = []
	processed = []
	# Comparing elements in projects
	for i in range(0, len(project_objs)):
		if project_objs[i] in processed:
			continue
		list_of_i_dups = []
		ith_obj = project_objs[i]
		for j in range(i+1, len(project_objs)):
			if ith_obj == project_objs[j]:
				continue # Dont compare same object
			if(isduplicate(ith_obj,project_objs[j])):
				if len(list_of_i_dups)==0:
					list_of_i_dups.append(ith_obj)
					processed.append(ith_obj)
				list_of_i_dups.append(project_objs[j])
				processed.append(project_objs[j])
		if len(list_of_i_dups) !=0:
			duplicate_projects.append(list_of_i_dups)
	return duplicate_projects

def print_duplicate_projects_results(duplicate_projects,SLNET_loc):
	counter =1
	duplicates_remove = 0
	number_models_duplicates =0
	with open(os.path.join(SLNET_loc,"potential_duplicates_list.csv"),'w') as f:
		f.write("S.N.,Duplicate Project IDs,No. of Duplicates\n")
		for dup_lst in duplicate_projects:
			dup_id = [project.id for project in dup_lst]
			p_ids = ",".join([str(project.id) for project in dup_lst])
			f.write(str(counter)+" "+p_ids+","+str(len(dup_id)-1)+"\n")

			duplicates_remove += len(dup_id)-1
			number_models_duplicates += ((len(dup_id)-1)*len(dup_lst[0].model_files))
			counter+=1
	logging.info ("Number of duplicate Projects to remove :{}".format(duplicates_remove))
	logging.info("Number of Simulink models in duplicate Projects :{}".format(number_models_duplicates))

def keep_project(lst_ids,github_ids):
	
	for project_id in lst_ids:
		if project_id in github_ids: 
			return project_id
	lst_ids.sort()
	return lst_ids[0]

def remove_from_database(p_id,source,conn):
	subsys_table = source+"_subsys_info"
	hierar_table = source+"_hierar_info"
	block_table = source+"_block_info"
	metric_table = source+"_metric"
	project_table = source+"_projects"

	cur = conn.cursor()
	

	tables = [subsys_table,hierar_table,block_table,metric_table]
	for table in tables: 
		sql = "Delete from "+table+" where file_id = "+str(p_id)
		logging.info(sql)
		try:
			cur.execute(sql)
			conn.commit()
		except Error as e:
			logging.error(e)
	sql = "Delete from "+project_table+" where id = "+str(p_id)
	logging.info(sql)
	try:
		cur.execute(sql)
		conn.commit()
	except Error as e:
		logging.error(e)


def move_from_slnet(conn, duplicate_projects,SLNET_loc,db_name):
	#Copy of db 
	name,ext = db_name.split(".")
	shutil.copyfile(os.path.join(SLNET_loc,db_name),os.path.join(SLNET_loc,name+"_with_duplicates."+ext))
	github_ids = get_github_project_id(conn)
	duplicates_folder = os.path.join(SLNET_loc,"potential_duplicates")
	if not os.path.isdir(duplicates_folder):
		os.mkdir(duplicates_folder)
	
	for dup_lst in duplicate_projects:
		dup_id = [project.id for project in dup_lst]
		id_to_keep = keep_project(dup_id,github_ids)
		try: 
			for id in dup_id:
				if id == id_to_keep:
					continue
				else:

					filename = str(id)+".zip"
					if id in github_ids:
						remove_from_database(id,'GitHub',conn)
						shutil.move(os.path.join(SLNET_loc,"SLNET_GitHub",filename),os.path.join(duplicates_folder,filename))
					else:
						remove_from_database(id,'MATC',conn)
						shutil.move(os.path.join(SLNET_loc,"SLNET_MATLABCentral",filename),os.path.join(duplicates_folder,filename))
		except Exception as e:
			logging.error(e)



		






def main(conn,SLNET_loc,db_name):
	ids = get_project_id(conn)
	#Creatiing Project Objects
	project_objs = []
	for id in ids: 
		project_objs.append(Project(id,conn))


	print(len(project_objs))
	duplicate_projects = get_duplicate_projects(project_objs)
	print_duplicate_projects_results(duplicate_projects,SLNET_loc)

	move_from_slnet(conn, duplicate_projects,SLNET_loc,db_name)


if __name__ == '__main__':
	SLNET_loc = ""
	db_name  = "slnet_v1.sqlite"
	database = os.path.join(SLNET_loc,db_name)

	conn = create_connection(database)
	main(conn,SLNET_loc,db_name)