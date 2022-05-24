<html>
<body>
  <h1>Guía de usuario TFTP</h1>
      <ul>
        <li><a href="#iniciar">1. Configuración previa</a></li>
        <li><a href="#ejecucion">2. Ejecución del cliente</a></li>
        <li><a href="#config1">3. Cónfigurar opciones desde el cliente</a></li>
        <li><a href="#metodoselec">4. Selección del método (GET/PUT)</a></li>
        <ul>
            <li class="sub-li"><a href="#put">4.1 PUT</a></li>
            <li class="sub-li"><a href="#get">4.2 GET</a></li>
        </ul>
        <li><a href="#problemes">5. Problemas y resolución</a></li>
        
     </ul>
    <hr>
    <h2 id="iniciar">1. Configuración previa</h2>
    <p>
        Antes de empezar a usar el cliente, recomendamos revisar el archivo de Configuración
        <strong>settings.ini</strong>.
        <br>
        Este fichero contiene la siguiente información por defecto: <br>
        <br>
        <div class="coded">
            <code>
                [SERVEROPTIONS]<br>
                ;Server options<br>
                serverName = 127.0.0.1<br>
                serverPort = 12004<br>
                ; por defecto RRQ<br>
                opCode = 1 <br>
                packetSize = 512<br>
                mode = octet<br>
                timeOut = 4<br>
                
                [ERROR_PROMPT]<br>
                0 = "Error: NO IDENTIFICADO"<br>
                1 = "Error: ARCHIVO NO EXISTE"<br>
                2 = "Error: VIOLACION DE ACCESO"<br>
                3 = "Error: DISCO LLENO O EXCESO DE CAPACIDAD"<br>
                4 = "Error: OPERACION TFTP NO SOPORTADA"<br>
                5 = "Error: IDENTIFICADOR DE TRANSFERENCIA NO VALIDO"<br>
                6 = "Error: EL ARCHIVO YA EXISTE"<br>
                7 = "Error: USUARIO DESCONOCIDO"<br>
                <br>
            </code>
        </div>
        <br><br>
        Este archivo tiene cómo objetivo cargar una configuración por defecto en el cliente
        para que no sea necesario escribir la IP, puerto y el resto de configuraciones al iniciar el cliente.
        De este modo basta con configurar este archivo y ejecutar el cliente.
        <br><br>
        <ul class="desc">
            <p><strong>ServerName:</strong> IP del servidor que se quiere conectar.</p>
            <p><strong>ServerPort:</strong> Puerto del servidor que se quiere conectar.</p>
            <p><strong> OpCode:</strong> Opción que se quiere ejecutar (1 -> GET | 2-> PUT).</p>
            <p><strong> PacketSize:</strong> Tamaño del paquete que se quiere enviar.</p>
            <p><strong>Mode:</strong> Modo de transferencia (octet | netascii).</p>
            <p><strong>TimeOut:</strong> Tiempo de espera para la respuesta del servidor.</p>
        </ul>
        <br>
        <p><strong>NOTA:</strong> Es fundamental que el timeout y al packetSize sea identico al del servidor. De lo contrario resultará en un error 4 (OPERACION TFTP NO SOPORTADA).</p>

    </p>
    <p class="goup"><strong><a href="#top">Ir arriba</a></strong></p>
    <hr>
    <h2 id="ejecucion">2. Ejecución del cliente</h2>
    <p>
        Para ejecutar el cliente, abriremos un terminal y escribiremos el comando:<br>
        <div class="coded"><code>python3.exe TFTP_Client_Pascual-Alex_Guardiola-Gabriel.py</code></div> <br>
        En Linux: 
        <br><br>
        <div class="coded"><code>python3 TFTP_Client_Pascual-Alex_Guardiola-Gabriel.py</code></div>
    </p>
    <p class="goup"><strong><a href="#top">Ir arriba</a></strong></p>
    <hr>
    <h2 id="config1">3. Cónfigurar opciones desde el cliente</h2>
    <p>
        Una vez en ejecución, se nos preguntará si queremos cambiar las opciones:<br><br>
        <div class="coded">
            <code>
                ##############################################<br>
                #####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#####<br>
                #####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;UDP CLIENT - GET/PUT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#####<br>
                #####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Alex P. y Gabriel&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#####<br>
                #####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v4.0  RELEASE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; #####<br>
                #####&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#####<br>
                ##############################################<br>
                <br><br>
                
                ====================================<br>
                CONFIGURACION POR DEFECTO:<br>
                ====================================<br>
                - Nombre del servidor: 127.0.0.1<br>
                - Puerto: 12004<br>
                - Tamano de paquete: 512<br>
                - Modo: octet<br>
                - TimeOut (ms): 0.004<br>
                ====================================<br>
                CAMBIAR CONFIGURACION?(y/n): <br><br>

            </code>
        </div>
        Si respondemos "y" nos preguntará cada una de las opciones mostradas anteriormente. Tendremos que volver
        a introducirlas todas.<br><br>
        Si respondemos "n" se ejecutará el cliente con las opciones por defecto.<br><br>
        <strong>NOTA: </strong>en caso de perder el fichero <strong>settings.ini</strong>, puedes copiarlo de este documento.
    </p>
    <p class="goup"><strong><a href="#top">Ir arriba</a></strong></p>
    <hr>
    <h2 id="metodoselec">4. Selección del método (GET/PUT)</h2>
    <p>
        Ahora nos pedirá que escribamos el método que queremos utilizar. El programa acepta
        tanto mayusculas cómo minusculas. En caso de escribir algo que no sea soportado, te volverá
        a preguntar que quieres hacer.<br><br>
        <div class="coded">
            <code>
                [CLIENTE]: USANDO LA CONFIGURACION POR DEFECTO!!!<br>
                ====================================<br>
                - SERVIDOR TFTP: 127.0.0.1:12004 <br>
                - Modo: octet <br>
                - Tamaño de paquete: 512 <br>
                ====================================            <br>
                [GET/PUT]: <br>
                <br>
            </code>
        </div>
    </p>
    <p class="goup"><strong><a href="#top">Ir arriba</a></strong></p>
    <hr>
    <h3 id="put">4.1 PUT</h3>
    <p>
        Si se ha seleccionado PUT, el cliente preguntará la ruta ORIGEN + el archivo que queremos subir.<br><br>
        Cómo estamos en PUT, esta ruta ORIGEN es la ubicación en el CLIENTE. <br><br>

        <div class="coded">
            <code>
                ==================================== <br>
                [GET/PUT]: PUT <br>
                ==================================== <br>
                [CLIENTE]: USANDO METODO PUT <br>
                ==================================== <br>
                <br>
                RUTA ORIGEN: <br>
                - Donde está ubicado. Ejemplo: /home/alex/archivo.txt <br>
                > foobar/foo.txt  <br>
                <br><br>
            </code>
        </div>
        Ahora nos pedirá que escribamos la ruta DESTINO + el archivo.<br><br>
        En este caso, el DESTINO es la ruta donde queremos que se guarde el archivo en el SERVIDOR. <br><br>
        <div class="coded">
            <code>
                ==================================== <br>
                RUTA DESTINO: <br>
                - Donde lo guardas. Ejemplo: /home/alex/archivo.txt <br>
                > foobar/foo.txt <br>
                <br><br>
            </code>
        </div>
        Después le daremos a ENTER y comenzará la subida. La finalización correcta se indica así:<br><br>
        <div class="coded">
            <code>
                [CLIENTE]: Enviando DATA 4353 <br>
                [CLIENTE]: Recibe ACK 4353 <br>
                [CLIENTE]: Enviando DATA 4354 <br>
                [CLIENTE]: Recibe ACK 4354 <br>
                [CLIENTE]: files/ESPIRAL_GRAN.txt ENVIADO CON EXITO A ('127.0.0.1', 12004) <br>
                <br>
            </code>
        </div>
    </p>
    <h3 id="get">4.2 GET</h3>
    <p>
        Si se ha seleccionado GET, el cliente preguntará la ruta ORIGEN + el archivo que queremos obtener.<br><br>
        Cómo estamos en GET, esta ruta ORIGEN es la ubicación en el SERVIDOR. <br><br>

        <div class="coded">
            <code>
                ==================================== <br>
                [GET/PUT]: GET <br>
                ==================================== <br>
                [CLIENTE]: USANDO METODO GET <br>
                ==================================== <br>
                <br>
                RUTA ORIGEN: <br>
                - Donde está ubicado. Ejemplo: /home/alex/archivo.txt <br>
                > foobar/foo.txt  <br>
                <br><br>
            </code>
        </div>
        Ahora nos pedirá que escribamos la ruta DESTINO + el archivo.<br><br>
        En este caso, el DESTINO es la ruta donde queremos que se guarde el archivo en el CLIENTE. <br><br>
        <div class="coded">
            <code>
                ==================================== <br>
                RUTA DESTINO: <br>
                - Donde lo guardas. Ejemplo: /home/alex/archivo.txt <br>
                > foobar/foo.txt <br>
                <br><br>
            </code>
        </div>
        Después le daremos a ENTER y comenzará la descarga. La finalización correcta se indica así:<br><br>
        <div class="coded">
            <code>
                [CLIENTE]: Recibe DATA 4352 <br>
                [CLIENTE]: Enviando ACK 4352 <br>
                [CLIENTE]: Recibe DATA 4353 <br>
                [CLIENTE]: Enviando ACK 4353 <br>
                [CLIENTE]: foobar/foo.txt DESCARGADO CON ÉXITO. <br>
            </code>
        </div>
    </p>
    <p class="goup"><strong><a href="#top">Ir arriba</a></strong></p>
    <hr>
    <h2 id="problemes">5. Problemas y resolución</h2>
    <p>
        Este apartado está dedicado a recolectar los errores que hemos tenido a lo largo de las entregas.
        <br><br>
        <b>1. </b>Si se envian/reciben archivos que no son potencias de dos, se quedaban paquetes colgando y no terminaba.
        El problema era que teniamos unos Ifs innecesarios que evitaban que el programa continuase. La solución fue quitar todos esos Ifs
        y dejar solo uno que comprueba si el DATA recibido es un byte vacío.
        <br><br>
        <b>2. </b> Hasta la versión final no podiamos indicar rutas de destino y de origen. Sólo podiamos indicar el nombre del archivo. La solución
        a esto fue comprobar si la ruta existia, si no existia, creaba la ruta de directorios sin el archivo final y finalmente hacer un open 
        para crear el archivo donde se descargará el archivo.
        <br><br>
        <b>3. </b>Problemas en la codificación y decodificación de los paquetes RRQ y WRQ. Cuando enviaba
        el blksize y el timeout lo pasaba mal. Esto pasaba porque al enviar el paquete convertiamos el int en bytes y al hacer split de los /x00 (centinelas), el byte cero del integer de blksize tambien se eliminaba. <br>
        <br>Ejemplo: 512 -> \x02\x00 si hacemos un split de los centinelas para quedarnos solo las opciones, este 512 quedaria en /x02.

        <br><br>
        La solución fue pasar el integer a string, codificarlo y desde el receptor, pasarlo a string y finalmentea integer.
        <br><br>
        <b>4. </b>En el PUT llegaba a acomular muchos TimeOuts en cadena y llegaba a un punto en el que el
        programa se paraba porque el servidor estaba enviando al mismo tiempo que el cliente. Es decir, que ambos estaban enviando y 
        ninguno esperaba ni DATA ni ACK. <br><br>
        La solución aquí fue quitar un wait DATA que teniamos de más y reducir el Time Out.
    </p>
    <p class="goup"><strong><a href="#top">Ir arriba</a></strong></p>
    <hr>
   </body>
   </html>
