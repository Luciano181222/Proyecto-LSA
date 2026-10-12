package traductorlsa;

public class TraductorLSA {

    public static void main(String[] args) {
        
        System.out.println("Guardando nueva traducción en el historial...");
        
        
        boolean exito = HistorialDAO.guardarTraduccion(1, "ayuda");
        
        if (exito) {
            System.out.println("¡Éxito! El historial se guardó correctamente en MySQL.");
        } else {
            System.out.println("Hubo un error al intentar guardar.");
        }
        
    } 
    
} 