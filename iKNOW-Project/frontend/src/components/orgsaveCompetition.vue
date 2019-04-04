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
          <p class="card-p"><span class="card-span">竞赛级别</span>
            <span v-if="competition.level === 0">校级</span>
            <span v-else-if="competition.level == 1">市级</span>
            <span v-else-if="competition.level == 2">省级</span>
            <span v-else-if="competition.level == 3">国家级</span>
            <span v-else-if="competition.level == 4">国际级</span>
            <span v-else-if="competition.level == 5">自由</span>
          </p>
          <p class="card-p"><span class="card-span">赛事简介</span>
            {{competition.detail}}
          </p>
        </Col>
        <Col span="6" offset="1">
          <Button class="card-buttonone" type="info" @click="goManage(index)">前往管理</Button>
          <Button class="card-buttonone" type="success" @click="publishIsOk(index)">发布比赛</Button>
          <Button class="card-buttontwo" type="text" @click="competitionDetails(index)">查看竞赛详情<Icon type="forward" size="large"></Icon></Button>
        </Col>
      </Row>
    </Card>
  </div>
  <Modal v-model="publishModal" width="500">
    <p slot="header" style="color:#2d8cf0;text-align:center">
      <Icon type="information-circled"></Icon>
      <span>确认发布比赛</span>
    </p>
    <div style="text-align:center">
      <h3 style="color: red">请确保填写比赛信息完整,包括阶段设置,报名设置等</h3>
    </div>
    <div slot="footer">
      <Button type="info" size="large" long @click="publishCompetition">我已完成并确认发布比赛</Button>
    </div>
  </Modal>
</div>
</template>

<script>
export default {
  name: 'competitionCard',
  data () {
    return {
      publishModal: false,
      index: -1,
      competitions: []
    }
  },
  mounted () {
    var dataGet = {
      status: 0
    }
    this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/competition', {params: dataGet})
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      var len = res.competitions.length
      for (var i = 0; i < len; i++) {
        this.competitions.push(res.competitions[i])
        this.competitions[i].sponsor = JSON.parse(res.competitions[i].sponsor)
      }
    })
    .catch((response) => {
      this.$Message.error('获取比赛信息失败')
    })
  },
  methods: {
    goManage (index) {
      this.$router.push('/competitionmanage/' + this.competitions[index].id)
    },
    competitionDetails (index) {
      this.$router.push('/competitiondetails/' + this.competitions[index].id)
    },
    publishIsOk (index) {
      var res0
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/listPhase?id=' + this.competitions[index].id)
        .then((response) => {
          res0 = JSON.parse(response.bodyText)
          if (res0.length === 0) {
            this.$Notice.error({
              title: '比赛信息不完整',
              desc: '您还没有创建阶段，请在阶段管理一栏中创建一个阶段，在比赛报名设置一栏中为相应阶段设置报名表'
            })
          } else {
            this.publishModal = true
            this.index = index
          }
        }).catch((response) => {
        })
    },
    publishCompetition () {
      this.publishModal = false
      var data = {name: this.competitions[this.index].name, status: 1}
      this.$http.put(this.GLOBAL.baseUrl + 'api/competition/detail/' + this.competitions[this.index].id, data)
        .then((response) => {
          this.$Message.success('发布成功')
        }).catch((response) => {
          this.$Message.error('发布失败')
        })
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
        font-weight: 600;
        overflow: hidden;
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
        margin-top: 10px;
        padding:5px 10px;
        font-size: 16px;
    }
    .card-buttontwo{
        font-size: 16px;
    }
</style>
