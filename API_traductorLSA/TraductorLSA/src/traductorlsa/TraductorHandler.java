package traductorlsa;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.IOException;
import java.io.OutputStream;

public class TraductorHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        
        String query = exchange.getRequestURI().getQuery();
        String palabraBuscada = "";
        
        if (query != null && query.contains("palabra=")) {
            palabraBuscada = query.split("=")[1]; 
        }

        
        DiccionarioDAO dao = new DiccionarioDAO();
        String rutaGif = dao.buscarGif(palabraBuscada);

        String respuesta;
        
        
        if (rutaGif != null && !rutaGif.equals("No se encontró el GIF")) {
            respuesta = "{\"status\": \"OK\", \"palabra\": \"" + palabraBuscada + "\", \"gif\": \"" + rutaGif + "\"}";
            
            
            HistorialDAO.guardarTraduccion(1, palabraBuscada);
            
        } else {
            
            respuesta = "{\"status\": \"ERROR\", \"mensaje\": \"La palabra no está en el diccionario de LSA\"}";
        }

       
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
        exchange.sendResponseHeaders(200, respuesta.getBytes("UTF-8").length);

        OutputStream os = exchange.getResponseBody();
        os.write(respuesta.getBytes("UTF-8"));
        os.close();
        }
    }