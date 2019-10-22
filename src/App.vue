<template>
  <div id="app">
    <div class="container">
      <div class="header">
        <div class="header__title">
          <a href="/">CT DMV Wait Times &#x1F698;</a>
        </div>
        <div class="header__subtitle">When's the best time to go to DMV in Connecticut?</div>
      </div>
      <div class="menu">
        <ul class="menu__buttons">
          <li v-for="branch in branches" :key="branch.id" @click="toggleActive(branch)" :class="[branch.active ? 'menu__button_active' : 'menu__buttuon_inactive']">{{ branch.name }}</li>
        </ul>
      </div>
      <div class="main">
        <div class="filters" @change="requestData">
          <div>
            <label for="service">Service</label>
            <select class="filters__input" type='text' name='service' v-model="filters.service">
              <option v-for="service in services" :key="service" :value="service">{{ service }}</option>
            </select>
          </div>
          <div>
            <label for="freq">Time interval</label>
            <select class="filters__input" type='text' name='freq' v-model="filters.freq">
              <option value="Monthly">Over a month</option>
              <option value="Weekly">Over a week</option>
              <option value="Daily">Over a day</option>
            </select>
          </div>
          <div>
            <label for="freq">Data start</label>
            <input class="filters__input" type='date' name='st_date' v-model="filters.st_date">
          </div>
          <div>
            <label for="freq">Data end</label>
            <input class="filters__input" type='date' name='end_date' v-model="filters.end_date">
          </div>
        </div>
        <!-- <p>{{ buildUrl }}</p>
        <p>{{ results.wait_time_mins }}</p> -->
        <div class="chart">
          <BarChart :chart-data="data" :options="options"> </BarChart>
        </div>
      </div>
    </div>
    <div class="footer">
      <p>Conceived during a long wait at the DMV by <a href="https://alexpetralia.com" target="_blank">@alexpetralia</a>.</p>
    </div>
  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import BarChart from './components/BarChart'

export default {
    name: 'app',
    components: {
        BarChart
    },
    data() {
        return {
            BASE_API: 'https://ctdmv.herokuapp.com/api',
            services: [],
            branches: [],
            filters: {
                service: '',
                st_date: '',
                end_date: '',
                freq: 'Monthly',
            },
            results: {},
            data: {},
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        }
    },
    created() {
        this.getServices()
        this.getBranches()
        this.requestData()
    },
    computed: {
        buildUrl() {      
            let active_branch = (this.branches.filter(x => x.active)[0] || '').name || ''
            let freq = this.filters.freq.toLowerCase() || 'monthly'
            return `${this.BASE_API}/wait_times/${freq}/?branch=${active_branch}&service=${this.filters.service}` + 
                `&date_after=${this.filters.st_date}&date_before=${this.filters.end_date}`
        }
    },
    methods: {
        getServices() {
            axios.get(`${this.BASE_API}/services`)
                .then(response => response.data).then(results => {
                    this.services = results.map(x => x.name); 
                })
        },
        getBranches() {
            axios.get(`${this.BASE_API}/branches`).then(response => response.data)
                .then(results => {
                    this.branches = results.map(obj => ({...obj, active: false}))
                })
        },
        toggleActive(item) {
            item.active = !item.active;
            for (let idx in this.branches) {
                let branch = this.branches[idx]
                if (branch.name != item.name) { branch.active = false }
            }
            this.requestData()
        }, 
        convertAxisLabels(wait_times) {
            const labels = Object.keys(wait_times)
            if (this.filters.freq === 'Weekly') {
                const weekday_map = {
                    '1': 'Monday',
                    '2': 'Tuesday',
                    '3': 'Wednesday',
                    '4': 'Thursday',
                    '5': 'Friday',
                    '6': 'Saturday',
                    '7': 'Sunday',
                }
                return labels.map(x => weekday_map[x])
            }
            else if (this.filters.freq === "Monthly") {
                return labels.map(x => {
                    if (x[x.length - 1] == '1') {
                        return x + "st"
                    }
                    else if (x[x.length - 1] == '2') {
                        return x + "nd"
                    }
                    else if (x[x.length - 1] == '3') {
                        return x + "rd"
                    }
                    else {
                        return x + "th"
                    }
                })
            }
            else {
                return labels.map(x => {
                    let time = x.toString().substring(1, x.length - 1).replace(',', ':')
                    if (time.includes(":0")) {
                        time += '0'
                    }
                    return time
                })
            }
        },
        requestData() {
            axios.get(this.buildUrl).then(response => response.data)
                .then(response => {
                    this.results = response
                    let wait_times = response.wait_time_mins || {}
                    let labels = this.convertAxisLabels(wait_times)
                    let data = Object.values(wait_times).map(x => Math.round(x * 100)/100)
                    this.data = {
                        labels: labels,
                        datasets: [
                            {
                                label: "Wait times (mins)",
                                data: data,
                                backgroundColor: "rgba(153, 102, 255, .2)",
                                borderColor: "rgb(153, 102, 255)",
                                borderWidth: "1",
                            }
                        ]
                    } // end data
                })
        },
}
}
/*eslint-enable */
</script>

<style scoped>
:root {

}

*, *::before, *::after {
  margin: 0;
  box-sizing: border-box;
  font-family: Roboto, Nunito, Open Sans, sans serif;
}

.container {
  display: grid;
  max-width: 80vw;
  margin: 0 auto;
  grid-template-columns: minmax(0, 1fr);
  justify-items: center;
}

.header {
  padding: 1rem 2rem;
}

.header__title {
  color: black;
  font-size: 1.6rem;
  padding: 1rem 2rem;
  border-radius: 5px;
  letter-spacing: .05rem;
  text-align: center;
}

.header__title a {
  text-decoration: none;
  color: black;
}

.header__subtitle {
  text-align: center;
  line-height: 1.4rem;
  color: rgba(0, 0, 0, .8);
  font-style: italic;
}

.menu__buttons {
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
  list-style: none;
  padding: .5rem 1rem;
  background-color: rgba(0, 0, 0, .05);
  border-radius: 10px;
}

.menu__buttons li {
  color: #fff;
  background-color: rgba(0, 0, 220, .7);
  font-size: .8rem;
  text-transform: lowercase;
  border-radius: 10px;
  padding: .5rem;
  margin: .3rem .2rem;
  transition: transform .2s;
}

.menu__buttons li:hover {
  background-color: rgba(0, 0, 139, .75);
  transform: scale(1.05);
  cursor: pointer;
}

.menu_buttons li.menu__button_active {
  background-color: (0, 0, 139, .75);
  transform: scale(1.05);
  cursor: pointer;
}

.footer {
  display: flex;
  position: fixed;
  bottom: 0;
  width: 100%;
  justify-content: center;
  align-items: center;
  padding: 0 1rem;
  background-color: black;
  min-height: 1.5rem;
}

.footer p {
  font-family: Segoe UI;
  font-size: .8rem;
  color: white;
}

.footer > p > a {
  text-decoration: none;
  color: lightblue;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin: 0 auto;
}

.filters > div {
  padding: .25rem .5rem
}

.filters label {
  color: gray;
  font-size: .7rem;
}

.filters__input {
  display: block;
  padding: .5rem 1rem;
  border-radius: 5px;
  border: 1px solid lightgray;
  background-color: rgba(255, 255, 204, .1);
}

.main {
  margin-bottom: 2rem;
}
</style>
