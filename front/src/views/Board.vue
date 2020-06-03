<template>
    <div class="board">
        <div :key="budgetKey">Zalogowany jako {{myUsername}}. <br> Budżet: {{budget}} <br> Stoisz na polu
            {{currentField}}.
        </div>
        <div class="first_part_board">
            <v-sheet
                    :width="field.width"
                    :height="field.height"
                    v-for="(field, index) in firstQuarterConfig"
                    :key="index"
                    :color="field.color"
                    class="first_quarter_fields"
            >
                                       <span style=" outline: 3px solid blue;">
                   {{field.id}}
                  </span>
                <span v-if="field.price != null">{{field.price}}$
                  <span v-if="field.owner != null">
                    owner:{{field.owner}}
                  </span>
                </span><br>
                <span v-if="field.type=='START'"><b>START</b></span>
                <v-icon small v-for="(id, house) in field.houses" :key="id.toString() + house.toString()">mdi-home
                </v-icon>
                <v-icon small v-for="user in field.users" :key="user.toString()">mdi-numeric-{{user}}-box-outline
                </v-icon>
                <v-icon x-large v-if="field.type=='CARD'">mdi-cards-outline</v-icon>
                <v-icon x-large v-if="field.type=='JAIL'">mdi-handcuffs</v-icon>
                <v-icon x-large v-if="field.type=='PAY'">mdi-cash-100</v-icon>
                <v-icon x-large v-if="field.type=='TRANSPORT'">mdi-train</v-icon>
            </v-sheet>
        </div>
        <div class="middle_part">
            <div class="second_part_board">
                <v-sheet
                        :width="field.width"
                        :height="field.height"
                        v-for="(field, index) in secondQuarterConfig"
                        :key="index"
                        :color="field.color"
                        class="second_quarter_fields"
                >
                            <span style=" outline: 3px solid blue;">
                   {{field.id}}
                  </span>
                    <span v-if="field.price != null">{{field.price}}$
                  <span v-if="field.owner != null">
                    owner:{{field.owner}}
                  </span>
                </span><br>
                    <v-icon small v-for="(id, house) in field.houses" :key="id.toString() + house.toString()">mdi-home
                    </v-icon>
                    <v-icon small v-for="user in field.users" :key="user.toString()">mdi-numeric-{{user}}-box-outline
                    </v-icon>
                    <v-icon x-large v-if="field.type=='CARD'">mdi-cards-outline</v-icon>
                    <v-icon x-large v-if="field.type=='PAY'">mdi-cash-100</v-icon>
                    <v-icon x-large v-if="field.type=='TRANSPORT'">mdi-train</v-icon>
                    <v-icon x-large v-if="field.type=='POWER_PLANT'">mdi-transmission-tower</v-icon>
                </v-sheet>
            </div>
            <v-container class="inside_part">
                <v-container class="info">
                    <h2>{{dice}}</h2>
                </v-container>
                <v-container class="turn">
                    <h2>{{turn}}</h2>
                </v-container>
                <v-container v-show="visible_houses" class="house-buy">
                    <h2> Kupno domków</h2>
                    <v-container class="buy_houses_buttons">
                        <v-col sm="4" md="2">
                          <v-text-field
                            label="ID pola"
                            outlined
                            v-model="house_id"
                          ></v-text-field>
                        </v-col>
                        <v-col sm="4" md="2">
                          <v-text-field
                            label="ilość domków"
                            outlined
                            v-model="house_quantity"
                          ></v-text-field>
                        </v-col>
                        <v-card-actions>
                            <v-btn class="mr-4" @click="buyHouses">Kup</v-btn>
                        </v-card-actions>
                    </v-container>
                </v-container>
                <v-container class="turn_buttons">
                    <v-card-actions class="dice-button">
                        <v-btn v-show="visible_play" class="mr-4" @click="startTurn">Rzuc kostka</v-btn>
                    </v-card-actions>

                    <v-card-actions>
                        <v-btn v-show="visible_end" class="mr-4" @click="endTurn">Zakończ turę</v-btn>
                    </v-card-actions>
                </v-container>
            </v-container>
            <div class="fourth_part_board">
                <v-sheet
                        :width="field.width"
                        :height="field.height"
                        v-for="(field, index) in fourthQuarterConfig"
                        :key="index"
                        :color="field.color"
                        class="fourth_quarter_fields"
                >
                                   <span style=" outline: 3px solid blue;">
                   {{field.id}}
                  </span>
                    <span v-if="field.price != null">{{field.price}}$
                  <span v-if="field.owner != null">
                    owner:{{field.owner}}
                  </span>

                </span><br>
                    <v-icon small v-for="(id, house) in field.houses" :key="id.toString() + house.toString()">mdi-home
                    </v-icon>
                    <v-icon small v-for="user in field.users" :key="user.toString()">mdi-numeric-{{user}}-box-outline
                    </v-icon>
                    <v-icon x-large v-if="field.type=='CARD'">mdi-cards-outline</v-icon>
                    <v-icon x-large v-if="field.type=='TRANSPORT'">mdi-train</v-icon>
                    <v-icon x-large v-if="field.type=='PAY'">mdi-cash-100</v-icon>
                    <v-icon x-large v-if="field.type=='POWER_PLANT'">mdi-transmission-tower</v-icon>
                </v-sheet>
            </div>
        </div>

        <div class="third_part_board">
            <v-sheet
                    :width="field.width"
                    :height="field.height"
                    v-for="(field, index) in thirdQuarterConfig"
                    :key="index"
                    :color="field.color"
                    class="third_quarter_fields"
            >
                                       <span style=" outline: 3px solid blue;">
                   {{field.id}}
                  </span>
                <span v-if="field.price != null">{{field.price}}$
                  <span v-if="field.owner != null">
                    owner:{{field.owner}}
                  </span>
                </span><br>
                <v-icon small v-for="(id, house) in field.houses" :key="id.toString() + house.toString()">mdi-home
                </v-icon>
                <v-icon small v-for="user in field.users" :key="user.toString()">mdi-numeric-{{user}}-box-outline
                </v-icon>
                <v-icon x-large v-if="field.type=='CARD'">mdi-cards-outline</v-icon>
                <v-icon x-large v-if="field.type=='TRANSPORT'">mdi-train</v-icon>
                <v-icon x-large v-if="field.type=='POWER_PLANT'">mdi-transmission-tower</v-icon>
                <v-icon x-large v-if="field.type=='GO_TO_JAIL'">mdi-handcuffs</v-icon>
                <v-icon x-large v-if="field.type=='GO_TO_JAIL'">mdi-hand-pointing-up</v-icon>
                <v-icon x-large v-if="field.type=='EMPTY'">mdi-power-plug</v-icon>
                <v-icon x-large v-if="field.type=='EMPTY'">mdi-car</v-icon>
            </v-sheet>
        </div>
        <div >
            <v-card
                    class="mx-auto"
                    max-width="200"
                    tile
                    :key="transaction1Key"
            >
                <v-list
                >
                    <v-subheader>Wysłane</v-subheader>
                    <v-list-item-group color="primary">
                        <v-list-item
                                v-for="(item, i) in sendByAuth"
                                :key="i"
                        >

                            <v-list-item-content>
                                <v-list-item-title>
                                    <v-text-field
                                            label="Pole"
                                            :value=item.field_id
                                    ></v-text-field>
                                    <v-text-field
                                            label="Cena"
                                            :value=item.price
                                    ></v-text-field>
                                    <v-text-field
                                            label="Sprzedaje"
                                            :value=item.seller.username
                                    ></v-text-field>
                                    <v-text-field
                                            label="Kupuje"
                                            :value=item.buyer.username
                                    ></v-text-field>
                                    <v-text-field v-if="!item.finished"
                                                  label="Status"
                                                  value="Aktywna"
                                    ></v-text-field>
                                    <v-text-field v-else
                                                  label="Status"
                                                  value="Zakończona"
                                    ></v-text-field>
                                    <div class="text-center" v-if="!item.finished">
                                        <v-btn small outlined color="indigo" @click="cancelTransaction(item.id)">Anuluj
                                        </v-btn>


                                    </div>
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-card>
            <v-card
                    class="mx-auto"
                    max-width="200"
                    tile

            >
                <v-list  :key="transaction2Key"
                >
                    <v-subheader>Otrzymane</v-subheader>
                    <v-list-item-group color="primary">
                        <v-list-item
                                v-for="(item, i) in sendByOthers"
                                :key="i"
                        >

                            <v-list-item-content>
                                <v-list-item-title>
                                    <v-text-field
                                            label="Pole"
                                            :value=item.field_id
                                    ></v-text-field>
                                    <v-text-field
                                            label="Cena"
                                            :value=item.price
                                    ></v-text-field>
                                    <v-text-field
                                            label="Sprzedaje"
                                            :value=item.seller.username
                                    ></v-text-field>
                                    <v-text-field
                                            label="Kupuje"
                                            :value=item.buyer.username
                                    ></v-text-field>
                                    <v-text-field v-if="!item.finished"
                                                  label="Status"
                                                  value="Aktywna"
                                    ></v-text-field>
                                    <v-text-field v-else
                                                  label="Status"
                                                  value="Zakończona"
                                    ></v-text-field>
                                    <div class="text-center" v-if="!item.finished">
                                        <v-btn small outlined color="indigo" @click="acceptTransaction(item.id)">
                                            Akceptuj
                                        </v-btn>
                                        <v-btn small outlined color="indigo" @click="cancelTransaction(item.id)">Odrzuć
                                        </v-btn>
                                    </div>
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-card>
        </div>
        <v-card
                class="mx-auto"
                max-width="200"
                tile
        >
            <v-list
            >
                <v-subheader>Nowa transakcja</v-subheader>

                <v-list-item
                >

                    <v-list-item-content>
                        <v-list-item-title>
                            <v-text-field
                                    v-model="transaction.field"
                                    label="field"
                                    :value=transaction.field
                            ></v-text-field>
                            <v-text-field
                                    v-model="transaction.price"
                                    label="price"
                                    :value=transaction.price
                            ></v-text-field>
                            <v-text-field
                                    v-model="transaction.isBuyingOffer"
                                    label="isBuyingOffer"
                                    :value=transaction.isBuyingOffer
                            ></v-text-field>
                            <v-select
                                    v-if="transaction.isBuyingOffer!=='true'"
                                    v-model="transaction.buyer"
                                    :items="playingUsers"
                                    label="buyer"
                                    item-text="user"
                                    item-value="user_id"
                            ></v-select>
                            <v-select
                                     v-if="transaction.isBuyingOffer!=='false'"
                                    v-model="transaction.seller"
                                    :items="playingUsers"
                                    label="seller"
                                    item-text="user"
                                    item-value="user_id"
                            ></v-select>


                            <div class="text-center">
                                <v-btn small outlined color="indigo" @click="newTransaction()">Wyślij
                                </v-btn>

                            </div>
                        </v-list-item-title>
                    </v-list-item-content>
                </v-list-item>

            </v-list>
        </v-card>
    </div>
</template>

<script>
    import axiosSessionBoard from "../utils/axiosSessionBoard"
    import {getToken} from "../utils/cookies";
    import baseUrl from "../config";

    export default {
        name: "Board",
        data: () => {
            return {
                boardConfig: {},
                transactionSocket: undefined,
                visible_play: false,
                visible_end: false,
                visible_houses: false,
                house_quantity: null,
                house_id: null,
                myTurn: false,
                turn: '',
                dice: null,
                message: '',
                // url_board: baseUrl + '/api/board/',
                url: "ws://0.0.0.0:8000",
                firstQuarterConfig: [],
                secondQuarterConfig: [],
                thirdQuarterConfig: [],
                fourthQuarterConfig: [],
                myUsername: "",
                jsonBoard: '',
                budget: '',
                playingUsers: [],
                transaction: {
                    price: 0,
                    field: 0,
                    isBuyingOffer: "true",
                    buyer: null,
                    seller: null
                },
                currentField: 1,
                fieldColors: [
                    "brown lighten-2",
                    "light-blue lighten-2",
                    "pink lighten-2",
                    "orange lighten-2",
                    "red lighten-2",
                    "yellow lighten-2",
                    "green lighten-2",
                    "blue lighten-2"
                ],
                items: [
                    {
                        avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
                        title: 'Brunch this weekend?',
                        subtitle: "<span class='text--primary'>Ali Connors</span> &mdash; I'll be in your neighborhood doing errands this weekend. Do you want to hang out?",
                    },
                    {
                        avatar: 'https://cdn.vuetifyjs.com/images/lists/2.jpg',
                        title: 'Summer BBQ <span class="grey--text text--lighten-1">4</span>',
                        subtitle: "<span class='text--primary'>to Alex, Scott, Jennifer</span> &mdash; Wish I could come, but I'm out of town this weekend.",
                    },
                    {
                        avatar: 'https://cdn.vuetifyjs.com/images/lists/3.jpg',
                        title: 'Oui oui',
                        subtitle: "<span class='text--primary'>Sandra Adams</span> &mdash; Do you have Paris recommendations? Have you ever been?",
                    },
                    {
                        avatar: 'https://cdn.vuetifyjs.com/images/lists/4.jpg',
                        title: 'Birthday gift',
                        subtitle: "<span class='text--primary'>Trevor Hansen</span> &mdash; Have any ideas about what we should get Heidi for her birthday?",
                    },
                    {
                        avatar: 'https://cdn.vuetifyjs.com/images/lists/5.jpg',
                        title: 'Recipe to try',
                        subtitle: "<span class='text--primary'>Britta Holt</span> &mdash; We should eat this: Grate, Squash, Corn, and tomatillo Tacos.",
                    },
                ],
                sendByAuth: [],
                sendByOthers: [],
                transaction1Key: 1,
                transaction2Key: 1,
                budgetKey: 1
            };
        },

        beforeMount() {
            this.fetchBoard()
            console.log("board")
            console.log(this.boardConfig)

            this.fetchTransactions()
            this.fetchUsername()
            this.fetchPlayingUsers()

        },
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
                this.boardSocket = new WebSocket(
                    this.url
                    + '/ws/game/' + '?token=' + getToken()
                );
                // this.lobbySocket.onopen = this.sendMessage

                this.boardSocket.onmessage = this.onMessage

                this.transactionSocket = new WebSocket(
                    this.url
                    + '/ws/transaction/' + '?token=' + getToken()
                );
                this.transactionSocket.onmessage = this.onMessageTransaction
            },
            onMessage(event) {
                let msg = JSON.parse(event.data);
                console.log(msg)

                switch (msg.action) {
                    case "update":
                        console.log((msg.board));
                        this.boardConfig = null;
                        this.boardConfig = msg.board;
                        // this.configureBoard();
                        // this.visible_play = true;
                        // document.getElementById("start_button").style.visibility = 'visible';
                        break;
                    case "turn":
                        this.setTurn(msg.your_turn, msg.username);
                        // dodałem zamykanie połączenia przed przejściem na inną stronę
                        // this.lobbySocket.close()
                        // this.$router.push('/board');
                        break;
                }
            },
            onMessageTransaction(event) {
                let msg = JSON.parse(event.data);
                console.log(msg)

                switch (msg.message) {
                    case "refresh":
                        this.fetchTransactions()
                        this.fetchUsername()
                        this.transactionKey+=1
                        this.budgetKey+=1
                        break;
                }
            },
            startTurn() {
                console.log("start turn");
                axiosSessionBoard.get(baseUrl + '/api/dice-roll/')
                    .then(response => {
                        console.log(response.data);
                        this.dice = "Rzuciłeś " + response.data["number"];
                        this.showBuyOption();
                        this.visible_play = false;
                        this.visible_end = true;
                        this.sendUpdate();
                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
            endTurn() {
                console.log("End Turn");
                this.boardSocket.send(JSON.stringify({
                    "action": "end_turn"
                }))
                this.visible_end = false;
                this.visible_houses = false;
            },
            showBuyOption() {
                this.visible_houses = true;
            },
            buyHouses() {
                console.log("buyHouses");
            },
            sendUpdate() {
                this.boardSocket.send(JSON.stringify({
                    "action": "update"
                }))
            },
            setTurn(myTurn, userTurn) {
                this.myTurn = myTurn;
                // console.log(response.data)
                if (this.myTurn === true) {
                    this.turn = "Twoja tura";
                    this.visible_play = true;
                } else {
                    this.turn = "Teraz gra " + userTurn;
                }
            },
            fetchTransactions() {
                axiosSessionBoard.get(baseUrl + '/api/transaction/')
                    .then(response => {
                        this.sendByAuth = response.data["send_by_auth"]
                        this.sendByOthers = response.data["send_by_others"]
                        console.log(response.data)
                        // this.message = "Wyrzucono: " + response.data.number + ", czyli stajesz na polu numer " + response.data.place_id;
                        // let place_id = response.data.place_id;

                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
            fetchUsername() {
                axiosSessionBoard.get(baseUrl + '/api/auth-user/')
                    .then(response => {
                        this.myUsername = response.data["username"]
                        this.budget = response.data["budget"]
                        this.currentField = response.data["field"]
                        this.setTurn(response.data["turn"], response.data["turn_user"])
                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
            fetchPlayingUsers() {
                axiosSessionBoard.get(baseUrl + '/api/playing-users/')
                    .then(response => {
                        this.playingUsers = response.data
                        console.log(this.playingUsers)

                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
            fetchBoard() {
                axiosSessionBoard.get(baseUrl + '/api/board/')
                    .then(response => {
                        console.log(response.data)
                        this.boardConfig = response.data
                        this.configureBoard()
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    });
            },
            configureBoard() {
                Object.entries(this.boardConfig).map((item, index) => {
                            if (
                                item[1].type === "GO_TO_JAIL" ||
                                item[1].type === "EMPTY" ||
                                item[1].type === "JAIL" ||
                                item[1].type === "START"
                            ) {
                                item[1].width = 120;
                                item[1].height = 120;
                                item[1].special_field = true;
                            } else {
                                item[1].special_field = false;
                            }

                            switch (item[1].zone) {
                                case 1:
                                    item[1].color = this.fieldColors[0];
                                    break;
                                case 2:
                                    item[1].color = this.fieldColors[1];
                                    break;
                                case 3:
                                    item[1].color = this.fieldColors[2];
                                    break;
                                case 4:
                                    item[1].color = this.fieldColors[3];
                                    break;
                                case 5:
                                    item[1].color = this.fieldColors[4];
                                    break;
                                case 6:
                                    item[1].color = this.fieldColors[5];
                                    break;
                                case 7:
                                    item[1].color = this.fieldColors[6];
                                    break;
                                case 8:
                                    item[1].color = this.fieldColors[7];
                                    break;
                                default:
                                    item[1].color = "grey lighten-4";
                            }

                            if (item[1].isPledged) {
                                item[1].color = "grey darken-1";
                            }

                            if (index < 11) {
                                if (!item[1].special_field) {
                                    item[1].width = 120;
                                    item[1].height = 60;
                                }

                                this.firstQuarterConfig.push(item[1]);
                            } else if (index >= 11 && index <= 19) {
                                if (!item[1].special_field) {
                                    item[1].width = 60;
                                    item[1].height = 120;
                                }
                                this.secondQuarterConfig.push(item[1]);
                            } else if (index > 19 && index <= 30) {
                                if (!item[1].special_field) {
                                    item[1].width = 120;
                                    item[1].height = 60;
                                }
                                this.thirdQuarterConfig.push(item[1]);
                            } else {
                                if (!item[1].special_field) {
                                    item[1].width = 60;
                                    item[1].height = 120;
                                }
                                this.fourthQuarterConfig.push(item[1]);
                            }
                        });
            },
            cancelTransaction(id) {
                axiosSessionBoard.delete(baseUrl + '/api/transaction/' + id)
                    .then(response => {
                        console.log("transakcja usunięta" + response)
                           this.transactionSocket.send(JSON.stringify({
                            'message': 'refresh',
                        }));
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    });
            },
            acceptTransaction(id) {
                axiosSessionBoard.put(baseUrl + '/api/transaction/' + id + '/')
                    .then(response => {
                        console.log("transakcja zakończona" + response)
                           this.transactionSocket.send(JSON.stringify({
                            'message': 'refresh',
                        }));
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    });
            },
            newTransaction() {
                console.log(this.transaction)
                axiosSessionBoard.post(baseUrl + '/api/transaction/', this.transaction)
                    .then(response => {
                        console.log("transakcja utworzona pomyślnie" + response)
                        this.transactionSocket.send(JSON.stringify({
                            'message': 'refresh',
                        }));
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    });
            }
        }


    };
</script>

<style scoped>
    .first_quarter_fields {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .first_part_board {
        flex-direction: column-reverse;
        display: flex;
    }

    .second_part_board {
        display: flex;
        flex-direction: row;
    }

    .board {
        margin: 0 2rem;
        display: flex;
    }

    .second_quarter_fields {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .third_quarter_fields {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .fourth_quarter_fields {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .fourth_part_board {
        display: flex;
        flex-direction: row-reverse;
    }

    .middle_part {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .turn, .dice {
        display: flex;
        justify-content: center;
    }

    .inside_part {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-content: center;
    }

    .house-buy {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .buy_houses_buttons, .turn_buttons {
        display: flex;
        align-items: center;
        justify-content: center;
    }

</style>
