
import logging
import sqlite3
from sqlite3 import Error
import sys
logging.basicConfig(filename='duplicates.log', filemode='a',
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
class Project():

	def __init__(self,id,conn):
		self.id = id
		self.conn = conn
		self.model_files = []
		mdl_metrics = self.get_model_data(id)
		for metric in mdl_metrics: 
			self.model_files.append(metric)

	def get_model_data(self,id):
	    """
	    Query tasks
	    :param conn: the Connection object
	    :param
	    :return:
    	"""
	    cur = self.conn.cursor()
	    sql = "select * from (select is_test , is_Lib, SCHK_Block_count, SLDiag_Block_count , C_corpus_blk_count , C_corpus_hidden_conn, C_corpus_conn, C_corpus_hierar_depth,"+\
	    " SubSystem_count_Top, Agg_SubSystem_count, Hierarchy_depth, LibraryLinked_Count, compiles, CComplexity, Sim_time , Alge_loop_Cnt , target_hw, solver_type,"+\
	    " sim_mode, total_ConnH_cnt, total_desc_cnt, ncs_cnt, scc_cnt , unique_sfun_count, sfun_nam_count, mdlref_nam_count, unique_mdl_ref_count from github_models "+\
	    "where file_id="+str(id)+" union select is_test , is_Lib, SCHK_Block_count, SLDiag_Block_count , C_corpus_blk_count , C_corpus_hidden_conn, C_corpus_conn,"+\
	    " C_corpus_hierar_depth, SubSystem_count_Top, Agg_SubSystem_count, Hierarchy_depth, LibraryLinked_Count, compiles, CComplexity, Sim_time , Alge_loop_Cnt ,"+\
	    " target_hw, solver_type, sim_mode, total_ConnH_cnt, total_desc_cnt, ncs_cnt, scc_cnt , unique_sfun_count, sfun_nam_count, mdlref_nam_count, unique_mdl_ref_count"+\
	    " from matc_models where file_id="+str(id) +") where is_Lib=0 and is_test!=1"
	    logging.info("SQL :"+sql)
	    cur.execute(sql)

	    rows = cur.fetchall()

	    return rows






def main():
	projectObj = Project()
	
if __name__ == '__main__':
    main()
