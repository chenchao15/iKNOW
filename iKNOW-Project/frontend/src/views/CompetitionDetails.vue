<template>
  <div>
    <navigationBar></navigationBar>
    <div class="poster">
      <img style="width:100%; height:450px" :src="competition.pic_url" />
    </div>
    <Row>
      <Col class="info">
        <Row class="info-first">
          <Col span="5">比赛名称</Col>
          <Col span="5">举办方</Col>
          <Col span="4">参赛队</Col>
          <Col span="5">报名截止时间</Col>
          <Col span="5">比赛开始时间</Col>
        </Row>
        <Row><hr color="#dddee1" size="2" /></Row>
        <Row class="info-second">
          <Col span="5">{{competition.title}}</Col>
          <Col span="5">{{competition.organizer}}</Col>
          <Col span="4">{{competition.team_number}}</Col>
          <Col span="5">{{competition.enrol_end_time}}</Col>
          <Col span="5">{{competition.start_time}} </Col>
        </Row>
      </Col>
    </Row>
    <Row class="content">
      <Col span="6" class="content-first">
        <Menu class="content-menu" active-name="基本信息" width="231px" :open-names="['比赛相关', '比赛信息']" @on-select="choosemenu">
          <Submenu name="比赛信息">
            <template slot="title">比赛信息</template>
            <MenuItem name="基本信息">基本信息</MenuItem>
            <MenuItem name="赛制安排">赛制安排</MenuItem>
            <MenuItem name="奖项设置">奖项设置</MenuItem>
            <MenuItem name="资料下载">资料下载</MenuItem>
          </Submenu>
          <div v-if="orgnizerFlag === 0">
            <Submenu name="比赛相关">
              <template slot="title">比赛相关</template>
              <MenuItem name="比赛入口">比赛入口</MenuItem>
              <MenuItem name="编辑信息">编辑信息</MenuItem>
              <MenuItem name="队伍管理" v-if="issingle === false">队伍管理</MenuItem>
              <MenuItem name="我的事件">我的事件</MenuItem>
            </Submenu>
          </div>
          <MenuItem name="公告">公告</MenuItem>
          <MenuItem name="讨论区">讨论区 </MenuItem>
          <div v-if="visitor_type === 'join' && loginFlag === 1">
            <MenuItem name="排行榜">排行榜 </MenuItem>
            <MenuItem name="历史记录">历史记录</MenuItem>
          </div>
          <div v-if="loginFlag === 1 && issingle === false">
            <MenuItem name="参赛队伍">参赛队伍</MenuItem>
          </div>
        </Menu>
      </Col>
      <Col span="14" class="content-second">
        <div  class="content-mainbody"> 
          <Row class="content-title">
            <h1 class="content-title-content">{{menu_name}}</h1>
          </Row>
          <Row class="content-style">
            <div v-if="menu_name === '比赛入口'">
              <competitionEntry :stageId="stageId"></competitionEntry>
            </div>
            <div v-else-if="menu_name === '队伍管理'">
              <teamManage :stageId="stageId"></teamManage>
            </div>
            <div v-else-if="menu_name === '编辑信息'">
              <editRegisterInfo :stageId="stageId"></editRegisterInfo>
            </div>
            <div v-else-if="menu_name === '我的事件'">
              <myEvent :stageId="stageId"></myEvent>
            </div>
            <div v-else-if="menu_name === '基本信息'">
              {{competition.content}}
            </div>
            <div v-else-if="menu_name === '赛制安排'">
              {{competition.scheduleArrangement}}
            </div>
            <div v-else-if="menu_name === '奖项设置'">
              {{competition.awardSetting}}
            </div>
            <div v-else-if="menu_name === '资料下载'">
              <materialDownload :stageId="stageId"></materialDownload>
            </div>
            <div v-else-if="menu_name === '参赛队伍'">
              <competitionTeams :stageId="stageId"></competitionTeams>
            </div>
            <div v-else-if="menu_name === '公告'">
              <informNotice :competitionId="competitionId"></informNotice>
            </div>
            <div v-else-if="menu_name === '讨论区'">
              <discussArea :competitionId="competitionId"></discussArea>
            </div>
            <div v-else-if="menu_name === '排行榜'">
              <leaderBoard :stageId="stageId"></leaderBoard>
            </div>
            <div v-else-if="menu_name === '历史记录'">
              <submitHistory :stageId="stageId"></submitHistory>
            </div>
          </Row>
        </div>
      </Col>
      <Col span="3" class="content-third">
        <div v-if="visitor_type === 'nojoin' && orgnizerFlag === 0 && loginFlag === 1">
          <Row>
            <h1 class="focus">比赛报名</h1>
          </Row>
          <Row class="button-focus-row">
            <Button v-if="isEnrol === false" class="button-focus button-enrol" @click="goEnrol">报 名</Button>
            <Button v-if="isEnrol === true" class="button-focus button-enrol remind-color" @click="goEnrol">已报名</Button>
          </Row>
        </div>
        <div v-if="visitor_type === 'join' && orgnizerFlag === 0 && loginFlag === 1">
          <Row>
            <h1 class="focus">比赛提醒</h1>
          </Row>
          <Row class="button-focus-row">
            <Button v-if="isRemind === false" class="button-focus button-enrol" @click="goRemind">提 醒</Button>
            <Button v-if="isRemind === true" class="button-focus button-enrol remind-color" @click="goRemind">已提醒</Button>
          </Row>
        </div>
        <div v-if="orgnizerFlag === 0 && loginFlag === 1">
          <Row>
            <h1 class="focus">比赛关注</h1>
          </Row>
          <Row class="button-focus-row">
            <Button v-if="isFocus === false" class="button-focus" @click="goFocus">关 注</Button>
            <Button v-if="isFocus === true" class="button-focus focus-color" @click="goFocus">已关注</Button>
          </Row>
          <Row class="button-focus-people">
            {{competition.focus_number}}人已关注
          </Row>
        </div>
        <Row>
          <h1 class="publisher">发布者</h1>
        </Row>
        <Row>
          <Button size="small" type="text" @click="goPripage">
            <Avatar class="publisher-avatar" :src="competition.avatar_url"/>
          </Button>
        </Row>
        <Row class="publisher-name">
          {{competition.publisher}}
        </Row>
        <div v-if="visitor_type === 'join' && orgnizerFlag === 0">
          <Row>
            <h1 class="focus">比赛退出</h1>
          </Row>
          <Row class="button-focus-row">
            <Button class="button-focus quit-color" @click="goQuit">退 出</Button>
          </Row>
        </div>
      </Col>
    </Row>
    <Modal v-model="quitflag" width="300" @on-ok="isquit">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>退出比赛</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <span>您确定要退出比赛吗？</span>
      </p>
      <Input v-model="quitcontent" type="textarea" :autosize="{minRows: 2,maxRows: 6}" placeholder="请输入退出比赛原因…"></Input>
    </Modal>
    <Footer></Footer>
  </div>
</template>
<script>
import navigationBar from '../components/navigationBar'
import Footer from '../components/footer'
import submitHistory from '../components/submitHistory'
import leaderBoard from '../components/leaderBoard'
import informNotice from '../components/informNotice'
import teamManage from '../components/teamManage'
import competitionTeams from '../components/competitionTeams'
import editRegisterInfo from '../components/editRegisterInfo'
import myEvent from '../components/myEvent'
import discussArea from '../components/discussArea'
import competitionEntry from '../components/competitionEntry'
import materialDownload from '../components/materialDownload'

export default {
  name: 'CompetitionDetails',
  props: ['stageId', 'competitionId'],
  data () {
    return {
      quitflag: false,
      quitcontent: null,
      issingle: false,
      button_type: 1,
      loginFlag: null,
      orgnizerFlag: null,
      visitor_type: 'join',
      menu_name: '基本信息',
      isFocus: false,
      isEnrol: false,
      isRemind: false,
      competition: { title: '', pic_url: '', status: '', organizer: '', publisher: '', scheduleArrangement: '', awardSetting: '', dataDownload: '', start_time: '', enrol_end_time: '', team_number: '', focus_number: '', content: '' }
    }
  },
  components: {
    navigationBar,
    Footer,
    submitHistory,
    leaderBoard,
    informNotice,
    teamManage,
    competitionTeams,
    editRegisterInfo,
    myEvent,
    discussArea,
    competitionEntry,
    materialDownload
  },
  created () {
    this.links()
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/competitiondetails/' + this.$route.params.id) {
        this.links()
      }
    }
  },
  methods: {
    links () {
      this.competitionId = this.$route.params.id
      this.getCookie()
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/state_update?id=' + this.$route.params.id)
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.competition.title = res.name
        this.competition.pic_url = res.pic_url
        this.competition.organizer = JSON.parse(res.sponsor)[0]
        this.competition.publisher = res.organizer.name
        this.competition.organizer_id = res.organizer.id
        this.competition.organizer_uid = res.organizer.uid
        this.competition.avatar_url = res.organizer.avatar_url
        this.competition.content = res.detail
        this.competition.team_number = res.team_number
        this.competition.focus_number = res.focus_number
        if (res.phase_enrolling) {
          this.competition.start_time = res.phase_enrolling[0].start_time
          this.competition.enrol_end_time = res.phase_enrolling[0].sign_end_time
          this.competition.stageId = res.phase_enrolling[0].id
          this.stageId = res.phase_enrolling[0].id
        } else if (res.phase_ongoing) {
          this.stageId = res.phase_ongoing[0].id
        }
      }).catch((response) => {
      })
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/and_contestant?id=' + this.$route.params.id)
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.stageId = res.current_phase.id
        if (res.current_phase.max_group === 1 && res.current_phase.min_group === 1) {
          this.issingle = true
        } else {
          this.issingle = false
        }
        if (res.is_focus === 0) {
          this.isFocus = false
        } else {
          this.isFocus = true
        }
        if (res.is_joining === 0) {
          this.isEnrol = false
          this.visitor_type = 'nojoin'
        } else if (res.is_joining === 1) {
          this.isEnrol = true
          this.visitor_type = 'nojoin'
        } else if (res.is_joining === 2) {
          this.isEnrol = true
          this.visitor_type = 'join'
        }
        if (res.is_remind === 0) {
          this.isRemind = false
        } else {
          this.isRemind = true
        }
      }).catch((response) => {
        // 当前用户和该比赛无关联
        this.isFocus = false
        this.isEnrol = false
        this.isRemind = false
        this.visitor_type = 'nojoin'
      })
    },
    // 读取 cookie
    getCookie () {
      if (document.cookie.length > 0) {
        var arr = document.cookie.split('; ') // 这里显示的格式需要切割一下自己可输出看下
        for (var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split('=') // 再次切割
          // 判断查找相对应的值
          if (arr2[0] === 'usertype') {
            this.orgnizerFlag = parseInt(arr2[1])  // 保存到保存数据的地方
          } else if (arr2[0] === 'islogin') {
            this.loginFlag = parseInt(arr2[1])  // 保存到保存数据的地方
          }
        }
      }
    },
    choosemenu: function (name) {
      this.menu_name = name
    },
    goEnrol () {   // 需想后端发送报名post
      if (this.isEnrol === false) {
        // this.isEnrol = true
        this.$router.push('/registerpage/' + this.$route.params.id + '/' + this.competition.stageId)
      }
      /* else {
        this.isEnrol = false
      } */
    },
    goFocus () {   // 需想后端发送关注post
      var dataPost
      if (this.isFocus === false) {
        dataPost = {
          competition_id: this.$route.params.id,
          status: 1
        }
      } else {
        dataPost = {
          competition_id: this.$route.params.id,
          status: 0
        }
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/collect_competition', dataPost)
      .then((response) => {
        this.isFocus = !this.isFocus
      })
      .catch((response) => {
      })
    },
    goQuit () {
      this.quitflag = true
    },
    isquit () {   // 需想后端发送退出post 退出理由this.quitcontent
      this.quitflag = false
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', {phase_id: this.stageId, event_type: 2, content: this.quitcontent, is_team: 1})
      .then((response) => {
        this.$Notice.success({
          title: '申请退赛审核中',
          desc: `申请退赛请求已发出，等待审核……`
        })
      })
      .catch((response) => {
        this.$Notice.error({
          title: '申请退赛请求失败',
          desc: `申请退赛请求失败……`
        })
      })
    },
    goPripage () {
      var type = 1
      var id = this.competition.organizer_id
      var mid = this.competition.organizer_uid
      this.$router.push('/otherUserPage/' + mid + '/' + id + '/' + type)
    },
    goRemind () {   // 需想后端发送提醒post
      if (this.isRemind === false) {
        this.$Notice.open({
          title: '提醒',
          desc: '在比赛开始之前，我们将会给您发邮件提醒您注意比赛时间',
          onClose: function () {
            alert('之后往后端发送要写邮件的内容')
          }
        })
        this.isRemind = true
      } else {
        this.$Notice.open({
          title: '取消提醒',
          desc: '您已经取消了比赛提醒',
          onClose: function () {
            alert('之后往后端发送取消提醒的邮件')
          }
        })
        this.isRemind = false
      }
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
    .info{
        margin: 20px 0px;
        text-align: center;
        border: 2px solid #dddee1;
    }
    .info-first{
        font-size: 16px;
        padding: 5px;
    }
    .info-second{
        color: #80848f;
        font-size: 12px;
        padding: 5px;
        font-weight: 400;
    }
    .button-style{
        position: relative;
        height: 100%;
    }
    .button-enrol1{
        width: 150px;
        border-radius: 0;
        padding: 17px;
        font-size: 22px;
        border: 0;
    }
    .button-enrol2{
        width: 150px;
        border-radius: 0;
        padding: 26px;
        font-size: 22px;
        border: 0;
    }
    .content{
        margin: 10px 0;
        border: 2px solid #dddee1;
    }
    .content-first{
        width: 230px;
        font-weight: 400;
    }
    .content-second{
        border: 2px solid #dddee1;
        min-height: 686px;   /* 手动设定高度 */
        border-bottom: 0;
        border-top: 0;
    }
    .content-third{
        padding: 40px 0 0 35px;
    }
    .content-menu{
        z-index: 0;
    }
    .content-mainbody{
        padding: 30px;
    }
    .content-title{
        border-left: 5px solid #80848f;
    }
    .content-title-content{
        padding-left: 10px;
        font-size: 23px;
        color: #666;
    }
    .content-style{
        font-weight: 400;
        padding-top: 20px;
        font-size: 16px;
    }
    .focus{
        border-left: 5px solid #80848f;
        padding-left: 20px;
        font-size: 20px;
    }
    .button-focus-row{
        padding: 25px 20px 10px 20px;
    }
    .button-focus{
        width: 80px;
        padding: 2px;
        font-size: 16px;
        background: white;
    }
    .button-focus-people{
        color: #80848f;
        font-size: 12px;
        padding-left: 20px;
        font-weight: 400;
    }
    .publisher{
        border-left: 5px solid #80848f;
        margin: 35px 0 20px 0;
        padding-left: 20px;
        font-size: 20px;
    }
    .publisher-avatar{
        margin: 0 0 10px 20px;
        width:60px;
        height:60px;
        border-radius: 70px;
    }
    .publisher-name{
        margin-bottom: 35px;
        color: #80848f;
        font-size: 14px;
        padding-left: 24px;
        font-weight: 400;
    }
    .button-enrol{
        margin-bottom: 25px;
    }
    .focus-color{
        border: 2px solid #ED3F14;
    }
    .remind-color{
        border: 2px solid #00B5FF;
    }
    .quit-color{
        /* border: 2px solid rgba(190, 25, 25, 0.56); */
    }
</style>
