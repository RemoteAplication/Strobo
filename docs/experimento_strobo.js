client = new Paho.MQTT.Client("mqtt.sj.ifsc.edu.br", Number("443"), "clientId");

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

client.connect({
  onSuccess: onConnect,
  keepAliveInterval: 30,
  //reconnect: true,
  //reconnectInterval: 10,
  useSSL: true
});

function onConnect() {
  console.log("onConnect");
  client.subscribe("arduino/remote_app");
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

function onMessageArrived(message) {
  console.log("onMessageArrived:" + message.payloadString);
};

function sendMessage(valor) {
  topic = "arduino/remote_app";
  message = new Paho.MQTT.Message(valor);
  message.destinationName = topic;
  client.send(message);
}
