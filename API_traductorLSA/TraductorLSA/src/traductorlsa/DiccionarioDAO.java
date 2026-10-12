package traductorlsa;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class DiccionarioDAO {

    
    public static String buscarGif(String palabraBuscada) {
        String rutaEncontrada = "No se encontró el GIF"; 
        
        
        String sql = "SELECT ruta_gif FROM diccionario WHERE palabra = ?";
        
        try {
            
            Connection con = Conexion.conectar();
            
            
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setString(1, palabraBuscada);
            
            
            ResultSet rs = ps.executeQuery();
            
            
            if (rs.next()) {
                rutaEncontrada = rs.getString("ruta_gif");
            }
            
          
            rs.close();
            ps.close();
            con.close();
            
        } catch (SQLException e) {
            System.out.println("Error al buscar en el diccionario: " + e.getMessage());
        }
        
        return rutaEncontrada; 
    }
}