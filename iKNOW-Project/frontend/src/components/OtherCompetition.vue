<template>
  <div class="other-competition">
    <div v-for="(i, index) in info" :key="i.id">
      <Col span="10" v-if="index % 2 === 0" style="margin-bottom: 15px">
        <Card style="width:320px; background:#dddee1">
          <div style="text-align:center">
            <a @click="clickDetail(i.id)"><img width="270px" height="150px" :src="i.pic_url"/></a>
            <h4>{{i.name}}</h4>
          </div>
        </Card>
      </Col>
      <Col span="10" offset="2" v-if="index % 2 !== 0" style="margin-bottom: 15px">
        <Card style="width:320px; background:#dddee1">
          <div style="text-align:center">
            <a @click="clickDetail(i.id)"><img width="270px" height="150px" :src="i.pic_url"/></a>
            <h4>{{i.name}}</h4>
          </div>
        </Card>
      </Col>
    </div>
  </div>
</template>

<script>
export default {
  name: 'other',
  props: ['id', 'type'],
  data () {
    return {
      info: []
    }
  },
  created () {
    this.links()
  },
  methods: {
    links () {
      var res
      if (this.type === 0) {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/other_contestant_competition?id=' + this.id)
          .then((response) => {
            res = JSON.parse(response.bodyText)
            this.info = res
          })
          .catch((response) => {
            this.$Message.error('获取比赛信息失败')
          })
      } else {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/other_organizer_competition?id=' + this.id)
          .then((response) => {
            res = JSON.parse(response.bodyText)
            this.info = res
          })
          .catch((response) => {
            this.$Message.error('获取比赛信息失败')
          })
      }
    },
    clickDetail (id) {
      this.$router.push('/competitiondetails/' + id)
    }
  }
}
</script>

<style>
    .other-competition{
        margin: 10px 50px;
    }
</style>
