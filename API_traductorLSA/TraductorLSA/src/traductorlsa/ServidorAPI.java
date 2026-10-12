
package traductorlsa;

import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;

public class ServidorAPI {
    public static void main(String[] args) throws Exception {
        
        HttpServer server = HttpServer.create(new InetSocketAddress(9000), 0);

        
        server.createContext("/api/traducir", new TraductorHandler());

       
        server.setExecutor(null); 
        server.start();
        
        System.out.println("Servidor SyncLSA encendido y escuchando en el puerto 8080...");
    }
}