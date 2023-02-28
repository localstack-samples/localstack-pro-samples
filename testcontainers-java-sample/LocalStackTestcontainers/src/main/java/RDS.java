import java.sql.*;

public class RDS {
    private static final String DEFAULT_USER = "test";
    private static final String DEFAULT_PW = "test";

    /**
     * Simple connection to test for demo purpose
     * Connects to an existing Postgres Database, creates a table, inserts some dummy data, and selects the data afterwards.
     *
     * @param hostname name of the database host
     * @param port port
     * @param dbname database name
     * @return String with the result of the select query
     *
     * @throws SQLException
     * @throws ClassNotFoundException
     */
    protected static String test_connection(String hostname, Integer port, String dbname) throws SQLException, ClassNotFoundException {
        Connection c = null;

        try {
            Class.forName("org.postgresql.Driver");
            String url = String.format("jdbc:postgresql://%s:%d/%s", hostname, port, dbname);
            c = DriverManager.getConnection(url, DEFAULT_USER, DEFAULT_PW);
            c.setAutoCommit(true);
            Statement stmt = c.createStatement();
            String sql = "CREATE TABLE HELLO " +
                    "(ID INT PRIMARY KEY     NOT NULL," +
                    " NAME           TEXT    NOT NULL) ";
            stmt.executeUpdate(sql);

            sql = "INSERT INTO HELLO (ID,NAME) "
                    + "VALUES (1, 'world');";
            stmt.executeUpdate(sql);
            ResultSet rs = stmt.executeQuery( "SELECT * FROM HELLO;" );
            String response = "";
            while( rs.next()) {
                int id = rs.getInt("id");
                String name = rs.getString("name");
                response += String.format("ID = %d\nNAME = %s", id, name);
            }
            rs.close();
            stmt.close();
            return response;
        } finally {
            try {
                c.close();
            } catch (SQLException e) {
                // we can ignore error here
            }
        }
    }

}
