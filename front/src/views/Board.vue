<template>
    <div class="board-all">
        <v-container class="log-info">
            <h3>{{message}}</h3>
        </v-container>
        <v-container :key="budgetKey">Zalogowany jako {{myUsername}}. Budżet: {{budget}}. Stoisz na polu
            {{currentField}}.
        </v-container>
        <div class="board">
        <v-container>
            <v-col>
                <v-row :key="boardKey">
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
                            <v-icon small v-for="(id, house) in field.houses"
                                    :key="id.toString() + house.toString()">
                                mdi-home
                            </v-icon>
                            <!--                <div v-if="field.users.length  > 0">-->
                            <v-icon small v-for="user in field.users" :key="user.toString()">
                                mdi-numeric-{{user}}-box-outline
                            </v-icon>
                            <!--                </div>-->

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
                                <v-icon small v-for="(id, house) in field.houses"
                                        :key="id.toString() + house.toString()">
                                    mdi-home
                                </v-icon>
                                <v-icon small v-for="user in field.users" :key="user.toString()">
                                    mdi-numeric-{{user}}-box-outline
                                </v-icon>
                                <v-icon x-large v-if="field.type=='CARD'">mdi-cards-outline</v-icon>
                                <v-icon x-large v-if="field.type=='PAY'">mdi-cash-100</v-icon>
                                <v-icon x-large v-if="field.type=='TRANSPORT'">mdi-train</v-icon>
                                <v-icon x-large v-if="field.type=='POWER_PLANT'">mdi-transmission-tower</v-icon>
                            </v-sheet>
                        </div>
                        <v-container class="inside_part">
                            <v-container class="dice">
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
                                                v-model="house.field"
                                        ></v-text-field>
                                    </v-col>
                                    <v-col sm="4" md="2">
                                        <v-text-field
                                                label="ilość domków"
                                                outlined
                                                v-model="house.number_of_houses"
                                        ></v-text-field>
                                    </v-col>
                                    <v-card-actions>
                                        <v-btn class="mr-4" @click="buyHouses">Kup</v-btn>
                                    </v-card-actions>
                                </v-container>
                            </v-container>
                            <v-container class="buy-button">
                                <v-card-actions>
                                    <v-btn v-show="visible_buy" class="mr-4" @click="buyProperty">Kup</v-btn>
                                </v-card-actions>
                            </v-container>
                            <v-container class="turn_buttons">
                                <v-card-actions class="dice-button">
                                    <v-btn v-show="user.isPlaying && !user.dice" class="mr-4" @click="startTurn">Rzuc kostka</v-btn>
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
                                <v-icon small v-for="(id, house) in field.houses"
                                        :key="id.toString() + house.toString()">
                                    mdi-home
                                </v-icon>
                                <v-icon small v-for="user in field.users" :key="user.toString()">
                                    mdi-numeric-{{user}}-box-outline
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
                            <v-icon small v-for="(id, house) in field.houses"
                                    :key="id.toString() + house.toString()">
                                mdi-home
                            </v-icon>
                            <v-icon small v-for="user in field.users" :key="user.toString()">
                                mdi-numeric-{{user}}-box-outline
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


                </v-row>

                <v-row>

                    <v-col>
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
                                                    <v-btn small outlined color="indigo"
                                                           @click="cancelTransaction(item.id)">
                                                        Anuluj
                                                    </v-btn>


                                                </div>
                                            </v-list-item-title>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list-item-group>
                            </v-list>
                        </v-card>
                    </v-col>
                    <v-col>
                        <v-card
                                class="mx-auto"
                                max-width="200"
                                tile

                        >
                            <v-list :key="transaction2Key"
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
                                                    <v-btn small outlined color="indigo"
                                                           @click="acceptTransaction(item.id)">
                                                        Akceptuj
                                                    </v-btn>
                                                    <v-btn small outlined color="indigo"
                                                           @click="cancelTransaction(item.id)">
                                                        Odrzuć
                                                    </v-btn>
                                                </div>
                                            </v-list-item-title>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list-item-group>
                            </v-list>
                        </v-card>
                    </v-col>
                    <v-col>
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
                                                <v-btn small outlined color="indigo" @click="newTransaction()">
                                                    Wyślij
                                                </v-btn>

                                            </div>
                                        </v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>

                            </v-list>
                        </v-card>
                    </v-col>
                </v-row>


            </v-col>
        </v-container>
    </div>
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
                // visible_play: false,
                visible_end: false,
                visible_houses: false,
                visible_buy: false,
                house: {
                    number_of_houses: null,
                    field: null,
                },
                user: {
                    id: null,
                    place: null,
                    isActive: false,
                    isPlaying: false,
                    budget: 0,
                    field_id: 0,
                    dice: false,
                    prison: false,
                    get_out_of_jail_card: 0
                },
                myTurn: false,
                turn: '',
                dice: null,
                message: "",
                // message: {
                //     action: null
                // },
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
                budgetKey: 1,
                boardKey: 1,

            };
        },

        beforeMount() {
            this.fetchBoard(true)
            console.log("board")
            console.log(this.boardConfig)

            this.fetchTransactions()
            this.fetchUserInfo()
            this.fetchPlayingUsers()
            this.fetchCurrentUser()
            this.fetchPlayingUser()

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
            },
            onMessage(event) {
                let msg = JSON.parse(event.data);
                console.log(msg)

                switch (msg.action) {
                    case "update":
                        console.log(msg.board);
                        this.boardConfig = msg.board;
                        this.configureBoard()
                        this.boardKey += 1
                        this.fetchUserInfo();
                        this.fetchPlayingUser();
                        console.log(this.user);
                        // this.fetchCurrentUser();
                        break;
                    case "turn":
                        this.setTurn(msg.your_turn, msg.username);
                        this.fetchUserInfo();
                        this.fetchPlayingUser();
                        break;
                    case "refresh_transaction":
                        this.boardConfig = msg.board;
                        this.configureBoard()
                        this.boardKey += 1
                        this.fetchTransactions()
                        this.fetchUserInfo()
                        this.transaction1Key += 1
                        this.transaction2Key += 1
                        // window.location.reload() todo: do uzgodnienia
                        this.budgetKey += 1
                        break;
                }
            },
            startTurn() {
                console.log("start turn");
                axiosSessionBoard.get(baseUrl + '/api/dice-roll/')
                    .then(response => {
                        console.log(response.data);
                        let msg = response.data
                        this.message = JSON.stringify(response.data) + "\n"
                        let card_msg = null;
                        if (msg["number"] == undefined) {
                            this.dice = msg
                        } else {
                            this.dice = "Rzuciłeś " + msg["number"];
                            this.showBuyOption();

                            switch (msg["action"]) {
                                case "normal card":
                                    this.stayOnField(msg);
                                    break;
                                case "transport":
                                    this.stayOnField(msg);
                                    break;
                                case "power_plant":
                                    this.stayOnField(msg);
                                    break;
                                case "get_card":
                                    card_msg = msg["card"];
                                    console.log(msg["card"]);
                                    console.log(card_msg);
                                    if (card_msg["action"] == "MOVE_TO" || card_msg["action"] == "MOVE" || "move" in card_msg) {
                                        this.stayOnField(card_msg["move"]);
                                    }
                                    break;
                            }
                        }

                        // this.visible_play = false;
                        this.visible_end = true;
                        // this.fetchBoard(false);
                        this.sendUpdate();
                    })
                    .catch(error => {
                        console.log(error);
                        this.message = error + "\n"
                    });
            },
            stayOnField(msg) {
                this.message = "Stanąłeś na " + msg["name"] + ". ";
                if ("my" in msg && msg["my"]) {
                    this.message +=  "To jest twoja posiadłość.";
                }
                if ("to_who" in msg) {
                    this.message +=  "To jest posiadłość " + msg["to_who"] + ". ";
                }
                if ("pay" in msg) {
                    this.message += "Musisz zaplacic M " + msg["pay"] + ".";
                }
                if (!("my" in msg || "to_who" in msg || "pay" in msg)) {
                    if ("price" in msg) {
                        this.visible_buy = true;
                        this.message += "Kosztuje " + msg["price"] + ". "
                    }

                }
            },
            endTurn() {
                console.log("End Turn");
                this.boardSocket.send(JSON.stringify({
                    "action": "end_turn"
                }))
                this.visible_end = false;
                this.visible_houses = false;
                this.visible_buy = false;
                this.dice = null;
            },
            showBuyOption() {
                this.visible_houses = true;
            },
            buyHouses() {
                console.log("buyHouses");
                axiosSessionBoard.post(baseUrl + '/api/field/buy-estate/', this.house)
                    .then(response => {
                        console.log("Zakup przeszedł pomyślnie" + response)
                        this.message += "Zakup przeszedł pomyślnie" + response+ "\n"
                        this.house.field = null
                        this.house.number_of_houses = null
                    })
                .catch(error => {
                        console.log(error.response.data);
                        this.message = error.response.data + "\n"
                });
            },
            buyProperty() {
                axiosSessionBoard.post(baseUrl + '/api/field/buy')
                    .then(response => {
                        console.log(response.data)
                        this.message += response.data + "\n"
                        this.visible_buy = false;
                    })
                .catch(error => {
                        console.log(error);
                        this.message = error.response.data + "\n"
                });
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
                    // this.visible_play = true;
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
            fetchUserInfo() {
                axiosSessionBoard.get(baseUrl + '/api/auth-user/')
                    .then(response => {
                        this.myUsername = response.data["username"]
                        this.budget = response.data["budget"]
                        this.currentField = response.data["field"]
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
            fetchBoard(first) {
                axiosSessionBoard.get(baseUrl + '/api/board/')
                    .then(response => {
                        console.log(response.data)
                        this.boardConfig = {}
                        // this.attachBoard(response.data)
                        this.boardConfig = response.data
                        if (first == true) {
                            this.configureBoard()
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    });
            },
            attachBoard(board) {
                console.log("ATTACHING BOARD")
                this.boardConfig = board;

                for (var key in board) {
                    var arr = [];
                    if (board[key].users != null) {
                        var users = board[key].users;
                        arr = Array.from(users)
                        console.log(key)
                        console.log(arr)
                        console.log(this.boardConfig[key].users)
                        this.boardConfig[key].users = null
                        this.boardConfig[key].users = Array.from(users)
                        this.boardConfig[key].users = arr
                        // this.boardConfig[key].users = Object.assign({}, this.boardConfig[key].users, arr);

                        console.log(this.boardConfig[key].users)
                        for (let i = 0; i < users.length; i += 1) {
                            // arr.push(users[i]);
                            console.log(users[i]);
                            // this.boardConfig["3"].users.splice(0, 1, 7)
                            this.$set(this.boardConfig["3"].users, i, [])
                            // this.boardConfig[key].users.splice(i, 1, users[i])
                            // Vue.set(this.boardConfig[key].users, i, users[i]);

                        }
                        // for (var i = 0; i < users.length; i += 1) {
                        //   Vue.set(this.boardConfig[key].users, i, users[i]);
                        // }
                    }
                }
                Object.entries(this.boardConfig).map((item, index) => {
                    // if (index + 1 ==)
                    if (item[1].users != null) {
                        console.log(item[1].users);
                        console.log(index)

                    }
                    // console.log(item[1].users);
                    // console.log(index);
                })
            },
            fetchCurrentUser() {
                axiosSessionBoard.get(baseUrl + '/api/current-user/')
                    .then(response => {
                        this.setTurn(response.data["turn"], response.data["turn_user"])
                    })
                    .catch(error => {
                        console.log(error);
                    })
            },
            fetchPlayingUser() {
                axiosSessionBoard.get(baseUrl + '/api/user/playing-user/')
                    .then(response => {
                        this.user = response.data;
                        if (this.user.isPlaying && this.user.dice) {
                            this.visible_end = true;
                        }
                    })
                    .catch(error => {
                        console.log(error);
                    })
            },
            configureBoard() {
                this.firstQuarterConfig = []
                this.secondQuarterConfig = []
                this.thirdQuarterConfig = []
                this.fourthQuarterConfig = []
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

                        this.boardSocket.send(JSON.stringify({
                            'action': 'refresh_transaction',
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
                        this.boardSocket.send(JSON.stringify({
                            'action': 'refresh_transaction',
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
                        this.boardSocket.send(JSON.stringify({
                            'action': 'refresh_transaction',
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

    .buy_houses_buttons, .turn_buttons, .buy-button {
        display: flex;
        align-items: center;
        justify-content: center;
    }

</style>
