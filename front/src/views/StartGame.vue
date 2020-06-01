<template>
  <div class="about">
    <v-container>
      <v-card>
        <h1>Witaj w poczekalni :) Za chwilę będziesz mógł rozpocząć grę</h1>
        <v-card-actions>
          <v-btn class="mr-4" style="visibility: hidden" @click="startGame">Rozpocznij grę</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </div>
</template>

<script>

    export default {
        data: () => ({
            reloaded: false,
            lobbySocket: undefined,
            url: 'ws://' // możliwe, że trzeba zmienić na 127.0.0.1:6379
        }),
        mounted() {
            if (localStorage.getItem('reloaded')) {
                // The page was just reloaded. Clear the value from local storage
                // so that it will reload the next time this page is visited.
                localStorage.removeItem('reloaded');
                this.prepareWebSocket()
            } else {
                // Set a flag so that we know not to reload the page twice.
                localStorage.setItem('reloaded', '1');
                location.reload();
            }
        },
        methods: {
            prepareWebSocket() {
                this.lobbySocket = new WebSocket(
                    this.url
                    + window.location.host
                    + '/ws/lobby/'
                );
                this.lobbySocket.onopen = this.sendMessage

                this.lobbySocket.onmessage = this.onMessage
            },
            startGame() {
                this.lobbySocket.send(JSON.stringify({
                    'type': 'start_clicked',
                }));
                // tutaj była te linijka, ale mam wątpliwości, czy na pewno o to chodziło, bo nie ma zmiennej boardName
                // do zmiany url lepiej tutaj używać this.$router.push(route)
                //TODO: co tutaj?
                // window.location.pathname = '/board/' + boardName + '/';
            },
            onMessage(event) {
                let msg = JSON.parse(event.data);

                switch (msg.message) {
                    case "load":
                        document.getElementById("start_button").style.visibility = 'visible';
                        break;
                    case "start":
                        document.getElementById("start_string").style.visibility = 'visible';
                        this.$router.push('/board');
                        // dodałem zamykanie połączenia przed przejściem na inną stronę
                        this.lobbySocket.close()
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