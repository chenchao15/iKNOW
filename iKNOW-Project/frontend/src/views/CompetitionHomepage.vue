<template>
  <div>
    <navigationBar></navigationBar>
    <div class="poster">
      <img style="width:100%; height:450px"  :src="competition.pic_url" />
    </div>
    <div class="content">
      <Col span="6">
        <Row class="com-info">
          <Row class="info-title">
            <h3 class="info-title-content">活动信息</h3>
          </Row>
          <Row>
            <div class="info-list">
              <Row class="info-item">
                <Col span="8">
                  <span class="info-item-label">比 赛：</span>
                </Col>
                <Col span="16">
                  <p class="info-item-content">{{competition.title}}</p>
                </Col>
              </Row>
              <Row><hr color="#eee" size="1" /></Row>
              <Row class="info-item">
                <Col span="8">
                  <span class="info-item-label">主办方：</span>
                </Col>
                <Col span="16">
                  <p class="info-item-content">{{competition.organizer}}</p>
                </Col>
              </Row>
              <Row><hr color="#eee" size="1" /></Row>
              <Row class="info-item">
                <Col span="8">
                  <span class="info-item-label">时 间：</span>
                </Col>
                <Col span="16">
                  <p class="info-item-content">开始 - </p>
                  <p class="info-item-content">{{competition.start_time}}</p>
                  <p class="info-item-content">结束 - </p>
                  <p class="info-item-content">{{competition.end_time}}</p>
                </Col>
              </Row>
            </div>
          </Row>
        </Row>
        <div class="info-detail">
          <Row class="info-title info-relate">
            <h3 class="info-title-content">活动详情</h3>
          </Row>
          <Row>
            <Button type="ghost" long class="button-detail" @click="goDetails">详 情</Button>
          </Row>
        </div>
      </Col>
      <Col span="18">
        <div  class="content-mainbody"> 
          <Row class="content-title">
            <h3 class="content-title-content">活动内容</h3>
          </Row>
          <Row class="content-style">
            {{competition.content}}
          </Row>
        </div>
      </Col>
    </div>
    <Footer></Footer>
  </div>
</template>
<script>
import navigationBar from '../components/navigationBar'
import Footer from '../components/footer'

export default {
  name: 'CompetitionHomepage',
  data () {
    return {
      competitionId: 0,
      competition: { title: '2017年APMCM亚太地区大学生数学建模竞赛', organizer: '河北省现场统计学会 亚太地区大学生数学建模竞赛组委会', pic_url: 'https://i.loli.net/2017/12/14/5a31dd532ad24.jpg', start_time: '2017年12月02日 00:45', end_time: '2018年03月31日 23:59', content: ' 新的时代，程序员想要跨入 AI 之门，首先要建立起全面的视野，培养充足的兴趣，并必须加强基础学习。人工智能实际上是一个将数学、算法理论和工程实践紧密结合的领域。人工智能扒开来看就是算法，也就是数学、概率论、统计学、各种数学理论的体现。想要在人工智能抓住机遇，加强基础理论——数学基础的学习，已经到了最紧迫的时刻！- 讲师简介 -徐老师211高校一线在职教师，哈尔滨理工大学应用数学硕士，德国明斯特大学计算机应用技' }
    }
  },
  components: {
    navigationBar,
    Footer
  },
  mounted () {
    this.links()
    this.competitionId = this.$route.params.id
  },
  methods: {
    links () {  // 获取比赛信息 比赛id：this.competitionId
    },
    goEnrol () {
      this.$router.push('/registerpage')
    },
    goDetails () {
      this.$router.push('/competitiondetails/' + this.competitionId)
    }
  }
}
</script>
<style scoped>
    .poster{
        text-align: center;
        padding: 10px 0 0px;
        border: 0px solid #d7dde4;
        background: #f5f7f9;
        z-index: 0;
    }
    .content{
        margin: 20px 0;
        width: 100%;
        height: 450px;
    }
    .com-p{
        font-size: 8px;
        color: #aaa;
        padding-left: 70px;
        position: relative;
    }
    .com-info{
        width: 250px;
        border: 1px solid #dddee1;
    }
    .info-title{
        background: #f8f8f9;
        height: 35px;
        border: 1px solid #e9eaec;
    }
    .info-title-content{
        padding: 5px 14px;
        text-align: left;
        font-size: 16px;
        color: #666;
        font-weight: 400;
    }
    .info-list{
        padding: 0 20px;
    }
    .info-item{
        padding: 10px 0;
        color: #666;
    }
    .info-item-label{
        line-height: 19px;
        font-size: 15px;
    }
    .info-item-content{
        line-height: 19px;
        color: #aaa;
        font-size: 12px;
    }
    .info-detail{
        margin: 20px 0;
        width: 250px;
        height: 100px;
        border: 1px solid #dddee1;
    }
    .button-detail{
        text-align: center;
        margin: 13px 50px;
        padding: 4px;
        background: white;
        width: 150px;
        font-size: 17px;
    }
    .button-focus{
        text-align: right;
    }
    .content-title{
        background: #f8f8f9;
        height: 35px;
        border: 1px solid #e9eaec;
    }
    .content-title-content{
        text-align: center;
        padding: 5px 14px;
        font-size: 16px;
        color: #666;
    }
    .content-mainbody{
        border: 1px solid #e9eaec;
    }
    .content-style{
        padding: 20px 40px;
        font-size: 18px;
        font-weight: 400;
    }
</style>
