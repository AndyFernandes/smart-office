import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.*;
import java.util.Timer;
import java.util.TimerTask;
import org.json.*;
import java.util.Random;

import java.util.Timer;
import java.util.TimerTask;
//Ar-condicionado
public class main {

    static byte[] sendData = new byte[1024];
    static DatagramPacket sendPacket;
    static DatagramSocket serverSocket;
    static DatagramSocket socket;


    public static void main(String args[]) throws IOException, JSONException {

        serverSocket = new DatagramSocket(null);
        serverSocket.setReuseAddress(true);
        String ip = InetAddress.getLocalHost().getHostAddress();
        InetSocketAddress address = new InetSocketAddress(ip, 5000);

        serverSocket.bind(address);
        String porta = "5001";
        int id = 1;
        String tipo = "Ar-condicionado";
        String status = "Ligado";
        int temperatura[] = new int[1];
        temperatura[0] = 30;


        ////////////////// CONEXAO BROADCAST
        byte[] receiveData = new byte[1024];

        DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
        System.out.println("Esperando por datagrama UDP na porta " + 5000);
        serverSocket.receive(receivePacket);

        String sentence = new String(receivePacket.getData());
        System.out.println(sentence);

        InetAddress IPAddress = receivePacket.getAddress();

        int port = receivePacket.getPort();

        String x = "{'id': "+ id +", 'tipo':'Ar-condicionado', 'ip': '" + ip + "', 'porta':" + porta + ", 'acoes':{'status': '"
                + status + "', 'temperatura':" + temperatura[0] + "}}";

        sendData = x.getBytes();

        sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, port);

        System.out.print("Enviando " + x + "...");

        serverSocket.send(sendPacket);
        System.out.println("OK\n");
        //serverSocket.close();


        socket = new DatagramSocket(null);
        address = new InetSocketAddress(ip, 5001);
        socket.bind(address);


        TimerTask task = new TimerTask() {
            @Override
            public void run() {
                Random aleatorio = new Random();
                temperatura[0] = temperatura[0] + (aleatorio.nextInt(2) - 1);
                System.out.print("temperatura eneviada\n");
                String p = "{'id': "+ id +", 'tipo':'Ar-condicionado', 'ip': '" + ip + "', 'porta':" + porta + ", 'acoes':{'status': '"
                        + status + "', 'temperatura':" + temperatura[0] + "}}";

                sendData = p.getBytes();

                sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, port);

                System.out.print("Enviando " + p + "...");

                try {
                    socket.send(sendPacket);
                }
                catch(IOException e) {
                    e.printStackTrace();
                }
            };
        };

        Timer timer = new Timer();
        long delay = 0;
        long intevalPeriod = 1 * 9000;
        // schedules the task to be run in an interval
        timer.scheduleAtFixedRate(task, delay,	intevalPeriod);

        while (true) {

            ////////////////// TESTANDO RECEBER
            receiveData = new byte[1024];
            sendData = new byte[1024];

            receivePacket = new DatagramPacket(receiveData, receiveData.length);
            System.out.println("Esperando por datagrama UDP na porta " + 5001);
            socket.receive(receivePacket);

            sentence = new String(receivePacket.getData());
            System.out.println(sentence);


        }
    }
}