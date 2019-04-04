<template>
<div class="card-div">
  <div v-for="(competition, index) in competitions" :key="competition.id">
    <Card class="card-card">
      <p slot="title" class="card-title">{{competition.name}}</p>
      <Row>
        <Col span="17">
          <p class="card-p"><span class="card-span">主办方</span>
            {{competition.sponsor[0]}}<span v-if="competition.sponsor.length > 1">等</span>
          </p>
          <p class="card-p"><span class="card-span">比赛级别</span>
            <span v-if="competition.level === 0">校级</span>
            <span v-else-if="competition.level == 1">市级</span>
            <span v-else-if="competition.level == 2">省级</span>
            <span v-else-if="competition.level == 3">国家级</span>
            <span v-else-if="competition.level == 4">国际级</span>
            <span v-else-if="competition.level == 5">自由</span>
          </p>
          <!--<p class="card-p" v-if="competition.status === 0"><span class="card-span">比赛状态</span>即将开始</p>
          <p class="card-p" v-if="competition.status === 1"><span class="card-span">比赛状态</span>进行中</p>
          <p class="card-p" v-if="competition.status === 2"><span class="card-span">比赛状态</span>已结束</p>-->
          <p class="card-p"><span class="card-span">赛事简介</span>
            {{competition.detail}}
          </p>
        </Col>
        <Col span="1" offset="2">
          <Button class="card-buttonone" type="info" @click="competitionDetails(index)">查看比赛详情</Button>
        </Col>
      </Row>
    </Card>
  </div>
</div>
</template>

<script>
export default {
  name: 'competitionCard',
  data () {
    return {
      competitions: []
    }
  },
  mounted () {
    var dataGet = {
      status: 1
    }
    this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/competition', {params: dataGet})
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      var len = res.competitions.length
      this.competitions = res.competitions
      for (var i = 0; i < len; i++) {
        this.competitions[i].sponsor = JSON.parse(res.competitions[i].sponsor)
      }
    })
    .catch((response) => {
      this.$Message.error('获取比赛信息失败')
    })
  },
  methods: {
    competitionDetails (index) {
      this.$router.push('/competitiondetails/' + this.competitions[index].id)
    }
  }
}
</script>

<style scoped>
    .card-div{
        padding: 10px;
        width: 800px;
        margin-left: -10%;
        margin-top: -5%;
    }
    .card-card{
        margin: 20px;
    }
    .card-title{
        text-align:center;
        display: inline-block;
        font-size: 18px;
        color: #666;
        line-height: 22px;
        font-weight: 600;
        overflow: hidden;
    }
    .card-span{
        position: absolute;
        left: 0;
        top: 0;
        color: #aaa;
        font-weight:
        600;overflow: hidden;
        text-overflow:ellipsis;
        white-space: nowrap;
    }
    .card-p{
        font-size: 14px;
        color: #aaa;
        line-height: 23px;
        padding-left: 70px;
        position: relative;
    }
    .card-buttonone{
        margin: 70% 0;
        padding:5px 10px;
        font-size: 18px;
    }
</style>
