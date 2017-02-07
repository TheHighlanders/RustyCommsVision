
/**
 *
 * AutoShutdown. Automatically shuts down Jetson at the end of the match.
 * @author David Matthews
 * @author Anmol Maini
 * @version Feb 7, 2017
 *
 */

import java.io.*;
import java.net.*;
import java.util.*;

public class AutoShutdown {

	private static DatagramSocket inputSocket;
	private static byte[] buffer;

	/**
	 * @param args
	 */
	public static void main(String[] args) throws IOException {

		init();
		// receive data and save
		while (true) {
			receiveAndProcessData();
		}
		inputSocket.close();
		
	}

	private static void init() {
		try {
			inputSocket = new DatagramSocket(5800);
		} catch (SocketException e) {
			System.out.println("DatagramSocket Failed to open");
		}

		buffer = new byte[256];
		newFile();
	}



	/**
	 * recieves data and stores it in buffer
	 */
	private static void receiveAndProcessData() {
		DatagramPacket dataPacket = new DatagramPacket(buffer, buffer.length);
		inputSocket.setSoTimeout(5000);
		inputSocket.receive(dataPacket);

		// parse to string
		String dataString = new String(dataPacket.getData(), 0, dataPacket.getLength());

		if (dataString.charAt(0) == 'e') {
`			shutDown();
		}
		 
	}


	private static void shutDown () {
		Process p = Runtime.getRuntime().exec("sudo shutdown -h now");
	}
}
