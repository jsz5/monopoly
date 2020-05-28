<template>
  <div class="board">
    <div class="first_part_board">
      <v-sheet
        :width="field.width"
        :height="field.height"
        v-for="(field, index) in firstQuarterConfig"
        :key="index"
        :color="field.color"
        class="first_quarter_fields"
        >
        <span v-if="field.price != null">{{field.price}}$
          <span v-if="field.owner != null">
            owner:{{field.owner}}
          </span>
        </span><br>
        <span v-if="field.type=='START'"><b>START</b></span>
        <v-icon small v-for="(id, house) in field.houses" :key="id.toString() + house.toString()">mdi-home</v-icon>
        <v-icon small v-for="user in field.users" :key="user.toString()">mdi-numeric-{{user}}-box-outline</v-icon>
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
           <span v-if="field.price != null">{{field.price}}$
          <span v-if="field.owner != null">
            owner:{{field.owner}}
          </span>
        </span><br>
          <v-icon small v-for="(id, house) in field.houses" :key="id.toString() + house.toString()">mdi-home</v-icon>
          <v-icon small v-for="user in field.users" :key="user.toString()">mdi-numeric-{{user}}-box-outline</v-icon>
          <v-icon x-large v-if="field.type=='CARD'">mdi-cards-outline</v-icon>
          <v-icon x-large v-if="field.type=='PAY'">mdi-cash-100</v-icon>
          <v-icon x-large v-if="field.type=='TRANSPORT'">mdi-train</v-icon>
          <v-icon x-large v-if="field.type=='POWER_PLANT'">mdi-transmission-tower</v-icon>
        </v-sheet>
      </div>
      <div class="fourth_part_board">
        <v-sheet
          :width="field.width"
          :height="field.height"
          v-for="(field, index) in fourthQuarterConfig"
          :key="index"
          :color="field.color"
          class="fourth_quarter_fields"
          >
              <span v-if="field.price != null">{{field.price}}$
          <span v-if="field.owner != null">
            owner:{{field.owner}}
          </span>
        </span><br>
          <v-icon small v-for="(id, house) in field.houses" :key="id.toString() + house.toString()">mdi-home</v-icon>
          <v-icon small v-for="user in field.users" :key="user.toString()">mdi-numeric-{{user}}-box-outline</v-icon>
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
        <span v-if="field.price != null">{{field.price}}$
          <span v-if="field.owner != null">
            owner:{{field.owner}}
          </span>
        </span><br>
        <v-icon small v-for="(id, house) in field.houses" :key="id.toString() + house.toString()">mdi-home</v-icon>
        <v-icon small v-for="user in field.users" :key="user.toString()">mdi-numeric-{{user}}-box-outline</v-icon>
        <v-icon x-large v-if="field.type=='CARD'">mdi-cards-outline</v-icon>
        <v-icon x-large v-if="field.type=='TRANSPORT'">mdi-train</v-icon>
        <v-icon x-large v-if="field.type=='POWER_PLANT'">mdi-transmission-tower</v-icon>
        <v-icon x-large v-if="field.type=='GO_TO_JAIL'">mdi-handcuffs</v-icon>
        <v-icon x-large v-if="field.type=='GO_TO_JAIL'">mdi-hand-pointing-up</v-icon>
        <v-icon x-large v-if="field.type=='EMPTY'">mdi-power-plug</v-icon>
        <v-icon x-large v-if="field.type=='EMPTY'">mdi-car</v-icon>
      </v-sheet>
    </div>
  </div>
</template>

<script>
export default {
  name: "Board",
  data: () => {
    return {
      boardConfig: {},
      firstQuarterConfig: [],
      secondQuarterConfig: [],
      thirdQuarterConfig: [],
      fourthQuarterConfig: [],
      fieldColors: [
        "brown lighten-2",
        "light-blue lighten-2",
        "pink lighten-2",
        "orange lighten-2",
        "red lighten-2",
        "yellow lighten-2",
        "green lighten-2",
        "blue lighten-2"
      ]
    };
  },
  beforeMount() {
    // axios
    //   .get("/user?ID=12345")
    //   .then(response => {
    //     // handle success
    //     console.log(response);
    //   })
    //   .catch(error => {
    //     // handle error
    //     console.log(error);
    //   });
    this.boardConfig = {
      "1": {
        type: "START",
        price: null,
        zone: null,
        owner: null,
        users: [1, 2]
      },
      "2": {
        type: "NORMAL_FIELD",
        price: 600,
        zone: 1,
        owner: 1,
        isPledged: false,
        houses: 3
      },
      "3": {
        type: "CARD",
        price: null,
        zone: null,
        owner: null
      },
      "4": {
        type: "NORMAL_FIELD",
        price: 600,
        zone: 1,
        owner: 2,
        isPledged: true,
        houses: 1
      },
      "5": {
        type: "PAY",
        price: null,
        zone: null,
        owner: null
      },
      "6": {
        type: "TRANSPORT",
        price: 2000,
        zone: null,
        owner: null
      },
      "7": {
        type: "NORMAL_FIELD",
        price: 1000,
        zone: 2,
        owner: null
      },
      "8": {
        type: "CARD",
        price: null,
        zone: null,
        owner: null
      },
      "9": {
        type: "NORMAL_FIELD",
        price: 1000,
        zone: 2,
        owner: null
      },
      "10": {
        type: "NORMAL_FIELD",
        price: 1200,
        zone: 2,
        owner: null
      },
      "11": {
        type: "JAIL",
        price: null,
        zone: null,
        owner: null
      },
      "12": {
        type: "NORMAL_FIELD",
        price: 1400,
        zone: 3,
        owner: null
      },
      "13": {
        type: "POWER_PLANT",
        price: 1500,
        zone: null,
        owner: null
      },
      "14": {
        type: "NORMAL_FIELD",
        price: 1400,
        zone: 3,
        owner: null
      },
      "15": {
        type: "NORMAL_FIELD",
        price: 1600,
        zone: 3,
        owner: null
      },
      "16": {
        type: "TRANSPORT",
        price: 2000,
        zone: null,
        owner: null
      },
      "17": {
        type: "NORMAL_FIELD",
        price: 1800,
        zone: 4,
        owner: null
      },
      "18": {
        type: "CARD",
        price: null,
        zone: null,
        owner: null
      },
      "19": {
        type: "NORMAL_FIELD",
        price: 1800,
        zone: 4,
        owner: null
      },
      "20": {
        type: "NORMAL_FIELD",
        price: 2000,
        zone: 4,
        owner: null
      },
      "21": {
        type: "EMPTY",
        price: null,
        zone: null,
        owner: null
      },
      "22": {
        type: "NORMAL_FIELD",
        price: 2200,
        zone: 5,
        owner: null
      },
      "23": {
        type: "CARD",
        price: null,
        zone: null,
        owner: null
      },
      "24": {
        type: "NORMAL_FIELD",
        price: 2200,
        zone: 5,
        owner: null
      },
      "25": {
        type: "NORMAL_FIELD",
        price: 2400,
        zone: 5,
        owner: null
      },
      "26": {
        type: "TRANSPORT",
        price: 2000,
        zone: null,
        owner: null
      },
      "27": {
        type: "NORMAL_FIELD",
        price: 2600,
        zone: 6,
        owner: null
      },
      "28": {
        type: "NORMAL_FIELD",
        price: 2600,
        zone: 6,
        owner: null
      },
      "29": {
        type: "POWER_PLANT",
        price: 1500,
        zone: null,
        owner: null
      },
      "30": {
        type: "NORMAL_FIELD",
        price: 2800,
        zone: 6,
        owner: null
      },
      "31": {
        type: "GO_TO_JAIL",
        price: null,
        zone: null,
        owner: null
      },
      "32": {
        type: "NORMAL_FIELD",
        price: 3000,
        zone: 7,
        owner: null
      },
      "33": {
        type: "NORMAL_FIELD",
        price: 3000,
        zone: 7,
        owner: null
      },
      "34": {
        type: "CARD",
        price: null,
        zone: null,
        owner: null
      },
      "35": {
        type: "NORMAL_FIELD",
        price: null,
        zone: 7,
        owner: null
      },
      "36": {
        type: "TRANSPORT",
        price: 2000,
        zone: null,
        owner: null
      },
      "37": {
        type: "CARD",
        price: null,
        zone: null,
        owner: null
      },
      "38": {
        type: "NORMAL_FIELD",
        price: 3500,
        zone: 8,
        owner: null
      },
      "39": {
        type: "PAY",
        price: null,
        zone: null,
        owner: null
      },
      "40": {
        type: "NORMAL_FIELD",
        price: 4000,
        zone: 8,
        owner: null
      }
    };

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

      if(item[1].isPledged){
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
</style>
