<template>
  <div class="about">
    <v-container>
      <v-card>
        <h1>Witaj w poczekalni :) Za chwilę będziesz mógł rozpocząć grę</h1>
        <div id="number_of_players">
          <h2>Liczba graczy: {{number}}</h2>
        </div>
        <v-card-actions>
          <v-btn v-show="visible" class="mr-4" @click="startGame">Rozpocznij grę</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </div>
</template>

<script>
    import {getToken} from "../utils/cookies"

    export default {
        data: () => ({
            reloaded: false,
            lobbySocket: undefined,
            number: 0,
            visible: false,
            url: 'ws://localhost:8000' // możliwe, że trzeba zmienić na 127.0.0.1:6379
        }),
        mounted() {
            if (localStorage.getItem('reloaded')) {
                // The page was just reloaded. Clear the value from local storage
                // so that it will reload the next time this page is visited.
                localStorage.removeItem('reloaded');
                this.prepareWebSocket()
                console.log(getToken())
            } else {
                // Set a flag so that we know not to reload the page twice.
                localStorage.setItem('reloaded', '1');
                location.reload();
            }
        },
        methods: {
            changeNumber(number) {
                this.number = number;
                return this.number;
            },
            prepareWebSocket() {
                this.lobbySocket = new WebSocket(
                    this.url
                    + '/ws/lobby/' + '?token=' + getToken()
                );
                // this.lobbySocket.onopen = this.sendMessage

                this.lobbySocket.onmessage = this.onMessage
            },
            startGame() {
                this.lobbySocket.send(JSON.stringify({
                    'type': 'start_clicked',
                }));
            },
            onMessage(event) {
                let msg = JSON.parse(event.data);
                console.log(msg)

                switch (msg.action) {
                    case "load":
                        this.visible = true;
                        // document.getElementById("start_button").style.visibility = 'visible';
                        this.changeNumber(msg.number)
                        break;
                    case "start":
                        this.visible = true;
                        // dodałem zamykanie połączenia przed przejściem na inną stronę
                        this.lobbySocket.close()
                        this.$router.push('/board');
                        break;
                  case "load_number":
                    // this.number = msg.number
                    this.changeNumber(msg.number)
                    break;

                }
            },
            sendMessage() {
                // Construct a msg object containing the data the server needs to process the message from the chat client.
                let msg = {
                    type: "joined",
                    date: Date.now()
                };

                // Send the msg object as a JSON-formatted string.
                this.lobbySocket.send(JSON.stringify(msg));
            }
        },
    };
</script>