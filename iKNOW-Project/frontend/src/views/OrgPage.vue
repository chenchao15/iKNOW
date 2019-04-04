<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
        <Row>
          <Col span="5">
            <Menu class="sidebar" :theme="chooseTheme" :active-name="chooseSelect" width="auto" :open-names="['competition', 'tutorial']" @on-select="chooseMenu">
              <MenuItem name="orginfo"><Icon type="person-stalker"></Icon>组织信息</MenuItem>
              <Submenu name="competition">
                <template slot="title">
                  <Icon type="ios-flag"></Icon>
                  比赛信息
                </template>
                <MenuItem name="saveCompetition">暂存中</MenuItem>
                <MenuItem name="goingCompetition">进行中</MenuItem>
                <MenuItem name="finishedCompetition">已结束</MenuItem>
              </Submenu>   
              <Submenu name="tutorial">
                <template slot="title">
                  <Icon type="ios-paper"></Icon>
                  教程信息
                </template>
                <MenuItem name="postTutorial">我发表的教程</MenuItem>
                <MenuItem name="saveTutorial">我暂存的教程</MenuItem>
              </Submenu>
              <MenuItem name="privateChat"><Icon type="ios-email"></Icon>私信</MenuItem>
            </Menu>
          </Col>
          <Col span="19">
            <div class="layout-content-main">
              <div v-if="sidebarMenu === 'orginfo'">
                <orgInfo></orgInfo>
              </div>
              <div v-else-if="sidebarMenu === 'saveCompetition'">
                <orgsaveCompetition></orgsaveCompetition>
              </div>
              <div v-else-if="sidebarMenu === 'goingCompetition'">
                <orggoingCompetition></orggoingCompetition>
              </div>
              <div v-else-if="sidebarMenu === 'finishedCompetition'">
                <orgfinishedCompetition></orgfinishedCompetition>
              </div>
              <div v-else-if="sidebarMenu === 'postTutorial'">
                <orgpostTutorial></orgpostTutorial>
              </div>
              <div v-else-if="sidebarMenu === 'saveTutorial'">
                <orgsaveTutorial></orgsaveTutorial>
              </div>
              <div v-else-if="sidebarMenu === 'privateChat'">
                <primsg></primsg>
              </div>
            </div>
          </Col>
        </Row>
      </div>
      <div class="layout-copy">
        2011-2017 &copy; iKNOW
      </div>
    </div>
  </div>
</template>
<script>
import navigationBar from '../components/navigationBar'
import orgInfo from '../components/orgInfo'
import orgfinishedCompetition from '../components/orgfinishedCompetition'
import orgsaveCompetition from '../components/orgsaveCompetition'
import orggoingCompetition from '../components/orggoingCompetition'
import orgpostTutorial from '../components/orgpostTutorial'
import orgsaveTutorial from '../components/orgsaveTutorial'
import primsg from '../components/primsg'

export default {
  name: 'OrgPage',
  data () {
    return {
      chooseTheme: 'light',
      sidebarMenu: 'orginfo',
      chooseSelect: 'orginfo',
      infoForm: {
        name: '',
        abbreviation: '',
        briefintro: '',
        address: '',
        field: '',
        linkman: '',
        phonenumber: '',
        mail: ''
      }
    }
  },
  components: {
    navigationBar,
    orgInfo,
    orgsaveCompetition,
    orggoingCompetition,
    orgfinishedCompetition,
    orgpostTutorial,
    orgsaveTutorial,
    primsg
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/orgpage') {
        this.sidebarMenu = 'orginfo'
        this.chooseSelect = 'orginfo'
      }
    }
  },
  methods: {
    chooseMenu: function (name) {
      this.GLOBAL.competitionType = name
      this.sidebarMenu = name
      this.chooseSelect = name
      this.$router.push('/orgpage')
    }
  }
}
</script>

<style scoped>
    .sidebar{
        background: #f8f8f9;
        z-index: 0;
    }
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        margin-top: 2%;
    }
    .layout-logo{
        width: 100px;
        height: 30px;
        background: #5b6270;
        border-radius: 3px;
        float: left;
        position: relative;
        top: 15px;
        left: 20px;
    }
    .layout-nav{
        width: 420px;
        margin: 0 auto;
    }
    .layout-assistant{
        width: 300px;
        margin: 0 auto;
        height: inherit;
    }
    .layout-breadcrumb{
        padding: 10px 15px 0;
    }
    .layout-content{
        min-height: 100%;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .layout-content-main{
        margin: 10px 100px 0px 100px;
        padding: 10px 25px 0 20px;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
</style>
