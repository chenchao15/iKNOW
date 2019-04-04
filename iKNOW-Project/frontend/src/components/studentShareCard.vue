<template>
<div>
  <div v-for="tutorial in tutorials" :key="tutorial.author.id">
    <Card class="card-card">
      <Row>
        <Col span="25">
          <Row>
            <Col span="8">
              <p class="card-title">
                {{tutorial.title}}
              </p>
            </Col>
            <Col span="1" offset="13">
              <Button class="card-buttonone" size="large" type="text" @click="tutorialDetails(tutorial.id)">教程详情<Icon type="forward" size="large"></Icon></Button>
            </Col>
          </Row>
          <p class="card-p"><span class="card-span">学友</span>
            {{tutorial.author.contestant_user.name}}
          </p>
          <p class="card-p"><span class="card-span">简介</span>
            {{tutorial.brief}}
          </p>
          <p class="card-p"><span class="card-span">创建时间</span>
            {{tutorial.post_time}}
          </p>
        </Col>
      </Row>
    </Card>
  </div>
</div>
</template>

<script>
export default {
  name: 'studentShareCard',
  props: ['type'],
  data () {
    return {
      tutorials: []
    }
  },
  mounted () {
    this.links()
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/officialTutorial') {
        this.links()
      }
    }
  },
  methods: {
    links () {
      this.tutorials = []
      if (this.type === '0') {
        this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/student_share')
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            this.tutorials = res0
          }).catch((response) => {
            this.$Message.error('失败')
          })
      } else if (this.type === '1') {
        this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/student_share?type=1')
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            this.tutorials = res0
          }).catch((response) => {
            this.$Message.error('失败')
          })
      } else {
        this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/student_share?type=2')
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            this.tutorials = res0
          }).catch((response) => {
            this.$Message.error('失败')
          })
      }
    },
    tutorialDetails (id) {
      this.$router.push('/tutorialDetails/' + id)
    }
  }
}
</script>

<style scoped>
    .card-card{
        margin: 30px;
        /* background: rgba(239, 242, 241, 0.3); */
    }
    .card-title{
        text-align:center;
        display: inline-block;
        font-size: 18px;
        color: #666;
        line-height: 22px;
        font-weight: 600;
        overflow: hidden;
        text-overflow:ellipsis;
        white-space: nowrap;
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
