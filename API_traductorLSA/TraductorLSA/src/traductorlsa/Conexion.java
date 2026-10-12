package traductorlsa;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Conexion {
    
   
    private static final String URL = "jdbc:mysql://localhost:3306/traductor_lsa";
    private static final String USER = "root"; 
    
    
    private static final String PASS = "123456"; 

    public static Connection conectar() {
        Connection conexion = null;
        try {
            
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            
            conexion = DriverManager.getConnection(URL, USER, PASS);
            System.out.println("¡Conexion exitosa a la base de datos traductor_lsa!");
            
        } catch (ClassNotFoundException e) {
            System.out.println("Error: Falta el archivo .jar del Connector.");
        } catch (SQLException e) {
            System.out.println("Error de conexión con MySQL: " + e.getMessage());
        }
        return conexion;
    }
}