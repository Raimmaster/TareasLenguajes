import scala.io.StdIn._
import java.net._
import java.io._

object Client {
	def main(args: Array[String]): Unit = {
		val server = new Socket(InetAddress.getByName("localhost"), 8888)
		val reader = new ObjectInputStream(server.getInputStream)
		val writer : ObjectOutputStream = new ObjectOutputStream(server.getOutputStream)
    	
    	readLine()

    	reader.close()
    	writer.close()
    	server.close()
	}
	
}