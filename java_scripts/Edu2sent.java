package learning;

import java.io.*;


public class Edu2sent{ // вырезает аннотации в формате "!.+", склеивает дискурсивные единицы в псевдопредложения, 
	//считает количество псевдопредложений, ЭДЕ, словоупотреблений
	// входной формат: 1 ЭДЕ на строке, граница между псевдопредложениями - пустая строка 
	// выходной формат: 1 псевдопредложение на строке, граница между псевдопредложениями - пустая строка

	 

	   
	
	   public static void main(String[] args) {
	       try{
	    	   final String encoding = "UTF-8";
	    	 
	    	   BufferedReader buf = new BufferedReader(new InputStreamReader(
	    			   new FileInputStream("C:\\ITMO\\itmove\\PARS\\0005\\0005.txt"), encoding)) ; 

	           Writer writer = new BufferedWriter(new OutputStreamWriter(
	        		   new FileOutputStream("C:\\ITMO\\itmove\\PARS\\tmp\\0005_ps.txt"), encoding)); 
			
	           // ArrayList<String> words = new ArrayList<>();
	           String lineJustFetched = null;
	           String tmp = ""; // 
	           int sent_counter = 0;
	           int token_counter = 0;
	           int edu_counter = 0;
	           
            //	
            	
				           while((lineJustFetched = buf.readLine()) != null){
				        	   
				        	   if (lineJustFetched.isEmpty() == false){
				        		   			edu_counter++; 
				        		   			
				        		   			String[] tokens = lineJustFetched.split("\\s+");
					        		   		
					        		        for (String token : tokens) {
					        		           if (token.contains("!") == false){				        		        	
					        		        	   token_counter++;
					        		        	   tmp  = tmp + " " + token;
					        		        	   //String lineJustFetched_removed_annot = lineJustFetched.replaceAll("(<split>|</split>)", "");
					        		        	   
				        		   	}
				        		   			
				        		   	}
				        	   }
				        	   else if (lineJustFetched.isEmpty() == true){ 	
				        		   		//writer.write("#sent_id = " + sent_counter + "\r\n"); 
				        		   		//writer.write("#text = " + tmp + "\r\n");
				        		        writer.write(tmp.trim() + "\r\n");
				        		        tmp = "";
				        		   		((BufferedWriter) writer).newLine();
				        		   		sent_counter++;
				        		   		
				        		   	}
			     	 
				           
				              	
				           }// closes while()
	           
			           	System.out.print("Number of sentences " + sent_counter + "\r\n");
		          		System.out.print("Number of elementary discourse units " + edu_counter + "\r\n");
		          		System.out.print("Number of tokens " + token_counter + "\r\n");
		          		buf.close();
		          		writer.close(); //closes try{}
	       
	      	
	   }
	      catch(Exception e){
	           e.printStackTrace();}
	      
	       
	           
	           }
}



