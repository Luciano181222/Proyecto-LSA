package traductorlsa;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class HistorialDAO {

    
    public static boolean guardarTraduccion(int idUsuario, String palabra) {
        
        
        String sql = "INSERT INTO historial (id_usuario, palabra_traducida) VALUES (?, ?)";
        
        try {
            Connection con = Conexion.conectar();
            PreparedStatement ps = con.prepareStatement(sql);
            
           
            ps.setInt(1, idUsuario);
            
            ps.setString(2, palabra);
            
            
            int filasAfectadas = ps.executeUpdate();
            
            ps.close();
            con.close();
            
          
            return filasAfectadas > 0;
            
        } catch (SQLException e) {
            System.out.println("Error al guardar en el historial: " + e.getMessage());
            return false;
        }
    }
}