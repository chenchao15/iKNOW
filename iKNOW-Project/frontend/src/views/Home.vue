<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <Carousel autoplay autoplay-speed="4000" v-model="startCarousel" loop>
        <CarouselItem v-for="(competition, index) in carouselCompetitions" v-if="index < 6" :key="index">
          <div class="carousel"><img @click="checkCompetitionDetails(competition.id)" style="width:100%; height:450px" :src="competition.pic_url" /></div>
        </CarouselItem>
      </Carousel>
    </div>
    <Tabs class="tab" type="card">
      <TabPane label="推荐竞赛" name="recommendCompetition"> 
        <Col span="8" v-for="(competition, index) in recommendCompetitions" v-if="index < 6" :key="index">
          <Card class="com-card">
            <div style="text-align:center">
              <img @click="checkCompetitionDetails(competition.id)" width="300px" height="150px" :src="competition.pic_url" />
              <h4>{{competition.name}}</h4>
            </div>
          </Card>
        </Col>
      </TabPane>
      <Button type="text" @click="checkAllCompetition" size="small" slot="extra">查看全部竞赛 <Icon type="arrow-right-a"></Icon></Icon></Button>
    </Tabs>
    <Tabs class="tab" type="card">
      <TabPane label="推荐教程" name="recommendTutorial">
        <Col span="11" offset="1" v-for="(tutorial, index) in recommendTutorials" :key="index">
          <Card class="com-card" @click="checkTutorialDetails(tutorial.id)">
            <div>
              <h4 style="text-align:center">{{tutorial.title}}</h4>
              <p>发布组织: {{tutorial.author.organizer_user.name}}</p>
              <p>教程简介: {{tutorial.brief}}</p>
            </div>
          </Card>
        </Col>
      </TabPane>
      <Button type="text" @click="checkAllTutorial" size="small" slot="extra">查看全部教程 <Icon type="arrow-right-a"></Icon></Icon></Button>
    </Tabs>
    <Footer></Footer>
  </div>
</template>
<script>
import navigationBar from '../components/navigationBar'
import Footer from '../components/footer'

export default {
  name: 'Home',
  data () {
    return {
      startCarousel: 0,
      carouselCompetitions: [],
      recommendCompetitions: [],
      recommendTutorials: []
    }
  },
  components: {
    navigationBar,
    Footer
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/home_competition')
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.carouselCompetitions = res
          this.recommendCompetitions = res
        })
        .catch((response) => {
          this.$Message.error('抱歉,您还未登录')
        })
      this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/offical_tutorial')
        .then((response) => {
          var res0 = JSON.parse(response.bodyText)
          this.recommendTutorials = res0
        }).catch((response) => {
          this.$Message.error('失败')
        })
      // get recommendTutorials（推荐教程数组）
    },
    checkCompetition (id) {
      this.$router.push('/competitionhomepage/' + id)
    },
    checkCompetitionDetails (id) {
      this.$router.push('/competitiondetails/' + id)
    },
    checkAllCompetition () {
      this.$router.push('/competitions')
    },
    checkTutorialDetails (id) {
      this.$router.push('/tutorialdetails/' + id)
    },
    checkAllTutorial () {
      this.$router.push('/tutorials')
    }
  }
}
</script>
<style scoped>
    .tab{
        margin-top: 20px;
    }
    .carousel{
        text-align: center;
    }
    .layout{
        border: 0px solid #d7dde4;
        background: #f5f7f9;
    }
    .com-card{
        width: 500px;
        background: #dddee1;
        margin-bottom: 15px;
    }
</style>
