<template>
  <div>
    <div v-for="notice in notices" :key="notice.id">
    <Card class="card-card">
      <Row>
        <Col span="25">
          <Row>
            <Col span="8">
              <p class="card-title">
                {{notice.title}}
              </p>
            </Col>
            <Col span="1" offset="13">
              <Button class="card-buttonone" size="large" type="text" @click="noticeDetails(notice.id)">公告详情<Icon type="forward" size="large"></Icon></Button>
            </Col>
          </Row>
          <Row>
            <Col class="card-p" span="10"><span class="card-span">创建时间</span>
              {{notice.post_time}}
            </Col>
          </Row>
          <p class="card-p"><span class="card-span">内容</span>
            {{notice.content}}
          </p>
        </Col>
      </Row>
    </Card>
  </div>
  </div>
</template>
<script>

export default {
  name: 'informNotice',
  props: ['competitionId'],
  data () {
    return {
      notices: []
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () { // 获取该比赛this.competitionId的公告内容赋给notices
      var dataGet = {
        competition_id: this.$route.params.id
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/notice', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.notices = res.posted_notices
        console.log(this.notices)
      })
    },
    noticeDetails (id) {
      this.$router.push('/noticeDetails/' + id)
    }
  }
}
</script>
<style scoped>
    .card-card{
        margin-bottom: 30px;
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
    }
    .card-p{
        font-size: 14px;
        color: #aaa;
        line-height: 23px;
        padding-left: 70px;
        position: relative;
    }
    .card-buttonone{
        padding:0;
        font-size: 15px;
    }
    .card-buttontwo{
        margin-top: 100%;
        margin-left: 80%;
        font-size: 16px;
    }
</style>