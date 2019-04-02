client = new Paho.MQTT.Client("mqtt.sj.ifsc.edu.br", Number("443"), "clientId"); // Precisamos definir no IFSC qual é a página

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;
client.connect({ onSuccess: onConnect, useSSL: true });

function onConnect() {
  console.log("onConnect");
  client.subscribe("arduino/remote_app");
  
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

function sendMessage(valor) {
  topic = "arduino/remote_app";
  //client.subscribe(topic);
  message = new Paho.MQTT.Message(valor);
  message.destinationName = topic;
  client.send(message);
}
