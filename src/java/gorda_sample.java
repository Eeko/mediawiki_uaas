public class QueryCache implements StatementExecutionListener, DatabaseStartupListener {
  private static RequestProcessor reqProc;
  private static LinkedHashMap cache = new LinkedHashMap() { protected boolean removeEldestEntry(Map.Entry entry) {
  };
}
return size() > 100;

public QueryCache(DatabaseProcessor dbProc, RequestProcessor reqProc, ReceiverStage stmtProc) {
  QueryCache.reqProc = reqProc; dbProc.setDatabaseStartupListener(this, true); stmtProc.setStatementExecutionListener(this, true);
}
public static void cacheLookup(String reqId, String query, ResultSet[] rs1) throws SQLException {
}
} rs1 = new ResultSet[1]; rs1[0] = s.executeQuery(cached); c.close();
90
  Connection c = DriverManager.getConnection("jdbc:default:connection"); Transaction tx = reqProc.getRequest(reqId).getTransaction();
Utils.info("looking up: txid=" + tx.getId());
java.sql.Statement s = c.createStatement(); String cached = (String) cache.get(query); if (cached == null) {
  Utils.info("not found, executing: " + query); ResultSet rs = s.executeQuery(query); cached = "values "; boolean first = true;
  while (rs.next()) { cached += "("; if (!first)
  cached += ", "; first = false; for (int i = 0; i < rs.getMetaData().getColumnCount(); i++) {
    if (i != 0) cached += ",";
    cached += "’" + rs.getString(i + 1) + "’"; cached += ")";
    } cache.put(query, cached);
  }

  public void handleStatementExecution(Statement statement) { try {
    switch (statement.getState()) { case Statement.PIPELINE_PROCESSING:
      if (statement.getStatement().toLowerCase().startsWith("select")) statement.setStatement("CALL cacheLookup(’"
        + statement.getRequest().getId() + "’, ’"
        + statement.getStatement() + "’)"); statement.continueExecution(); break;
      case Statement.PIPELINE_PROCESSED: statement.continueExecution(); break;
      case Statement.PIPELINE_ERROR: statement.continueExecution(); Utils.cleanUp(new SQLException("ObjectSet - WriteSet Error.")); break;
      } } catch (SQLException ex) {
        Utils.cleanUp(ex);
      }

    }
  }
  public void handleDatabaseStartup(Database database) { try {
  }
  switch (database.getContextState()) {
    case Database.DATABASE_STARTING: database.continueExecution(); break;
    case Database.DATABASE_UP: DataSource ds = database.getDataSource();
    Connection c = ds.getConnection();
    java.sql.Statement s = c.createStatement(); s.execute("CREATE PROCEDURE cacheLookup(reqid VARCHAR(10), query VARCHAR(100))"
      + "PARAMETER STYLE JAVA LANGUAGE JAVA READS SQL DATA DYNAMIC RESULT SETS 1"
      + "EXTERNAL NAME ’gorda.demo.QueryCache.cacheLookup’"); s.close(); c.close();
    database.continueExecution(); break;
    } } catch (SQLException ex) {
    }
    Utils.cleanUp(ex);