<template>
<div>
  <navigationBar></navigationBar>
  <div class="olay">
    <div class="olay-content">
      <div class="olay-content-main">
        <div class="olay-content-header">
          <img :src="person.avatar_url"/>
          <Button v-if="isOwn === 0" size="large" type="success" style= "margin-top: -270px;margin-left: 310px" @click="clickSendMsg">私信Ta</Button>
          <hr style="margin-top: -100px" color="#9ea7b4" size="2" />
          <hr style="margin-top: 10px" color="#bbbec4" size="2" />
          <hr style="margin-top: 10px" color="#c3cbd6" size="2" />
        </div>
        <Row>
          <Col span="5">
            <Menu style="z-index: 1" theme="light" :active-name="select" width="auto" :open-names="[ 'tutorial']" @on-select="chooseMenu">
              <MenuItem name="info" v-if="person.type === 0"><Icon type="person"></Icon>个人信息</MenuItem>
              <MenuItem name="info" v-if="person.type === 1"><Icon type="person"></Icon>组织信息</MenuItem>
              <MenuItem name="joinCompetition" v-if="person.type === 0"><Icon type="ios-flag"></Icon>Ta参加的比赛</MenuItem>
              <MenuItem name="createCompetition" v-if="person.type === 1"><Icon type="ios-flag"></Icon>Ta创建的比赛</MenuItem>
              <MenuItem name="postTutorial"><Icon type="ios-flag"></Icon>Ta的教程</MenuItem>
            </Menu>
          </Col>
          <Col span="19">
            <div>
              <div v-if="sidebarMenu === 'info'">
                <div class="other-info">
                  <div v-if="person.type === 0">
                    <p><strong>姓名：</strong>  {{person.name}}</p>
                    <p><strong>昵称：</strong> {{person.nickname}}</p>
                    <p v-if="person.gender === 1"><strong>性别：</strong> 男</p>
                    <p v-if="person.gender === 2"><strong>性别：</strong> 女</p>
                    <p><strong>所在高校：</strong> {{person.school}}</p>
                    <p><strong>专业：</strong> {{person.major}}</p>
                    <p><strong>自我介绍：</strong> {{person.introduction}}</p>
                  </div>
                  <div v-if="person.type === 1">
                    <p><strong>组织名称：</strong> {{person.name}}</p>
                    <p><strong>组织简称：</strong> {{person.shortname}}</p>
                    <p><strong>领域：</strong> {{person.field}}</p>
                    <p><strong>组织介绍：</strong> {{person.introduction}}</p>
                    <p><strong>组织联系人：</strong> {{person.contact}}</p>
                    <p><strong>联系电话：</strong> {{person.contact_number}}</p>
                    <p><strong>官方邮箱：</strong> {{person.contact_email}}</p>
                  </div>
                </div>
              </div>
              <div v-else-if="sidebarMenu === 'joinCompetition' || sidebarMenu === 'createCompetition'"><OtherCompetition :id="this.person.id" :type="this.person.type"></OtherCompetition></div>
              <div v-else-if="sidebarMenu === 'postTutorial'"><OtherPostTutorial :id="this.person.id" :type="this.person.type"></OtherPostTutorial></div>
            </div>
          </Col>
        </Row>
        <Modal title="私信Ta" v-model="sendModal" width="600">
          <div class="olay-modal">
            <div style="text-align: center">
              <Input class="card-modal-input" v-model="myMsg" type="textarea" :autosize="{minRows: 6,maxRows: 10}" placeholder="请输入要发送的信息．．．"></Input>
            </div>
          </div>
          <div slot="footer">
            <Button type="info" size="large" long :loading="modalLoading" @click="linkSendMsg">发送</Button>
          </div>
        </Modal>
      </div>
    </div>
    <div class="olay-copy">
      2011-2017 &copy; iKNOW
    </div>
  </div>
</div>
</template>

<script>
import navigationBar from '../components/navigationBar'
import OtherCompetition from '../components/OtherCompetition'
import OtherPostTutorial from '../components/OtherPostTutorial'
export default {
  name: 'forum',
  data () {
    return {
      select: 'info',
      sendModal: false,
      modalLoading: false,
      isOwn: 0,
      isType: -1,
      sidebarMenu: 'info',
      myMsg: '',
      person: {}
    }
  },
  components: {
    navigationBar,
    OtherCompetition,
    OtherPostTutorial
  },
  mounted () {
    this.links()
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/otherUserPage/' + this.$route.params.mid + '/' + this.$route.params.id + '/' + this.$route.params.type) {
        this.sidebarMenu = 'info'
        this.select = 'info'
        this.links()
      }
    }
  },
  methods: {
    links () {
      if (this.$route.params.type === '0') {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/con_detail/' + this.$route.params.id)
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.person = res
            this.person.type = 0
          })
          .catch((response) => {
            this.$Message.error('获取他人基本信息失败')
          })
      } else {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/org_detail/' + this.$route.params.id)
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.person = res
            this.person.type = 1
          })
          .catch((response) => {
            this.$Message.error('获取他人基本信息失败')
          })
      }
      this.getLoginStatusCookie()
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/login')
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          if (res.userid === parseInt(this.$route.params.id)) {
            if (parseInt(this.isType) === parseInt(this.$route.params.type)) {
              this.isOwn = 1
            } else {
              this.isOwn = 0
            }
          } else {
            this.isOwn = 0
          }
        })
        .catch((response) => {
        })
    },
    getLoginStatusCookie () {
      if (document.cookie.length > 0) {
        var arr = document.cookie.split('; ')
        for (var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split('=')
          if (arr2[0] === 'usertype') {
            this.isType = arr2[1]
          }
        }
      }
    },
    chooseMenu: function (name) {
      this.sidebarMenu = name
    },
    clickSendMsg () {
      this.sendModal = true
    },
    linkSendMsg () {
      this.modalLoading = true
      setTimeout(() => {
        this.modalLoading = false
        this.sendModal = false
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/personal_letter', {id: this.$route.params.mid, content: this.myMsg})
        .then((response) => {
          this.$Message.success('发送私信成功')
        })
        .catch((response) => {
          this.$Message.error('发送私信失败')
        })
        this.mymsg = ''
      }, 1500)
    }
  }
}
</script>

<style scoped>
    .olay{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
    }
    .olay-content{
        min-height: 200px;
        margin: 15px;
        padding: 50px;
        padding-top: 10px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .olay-content-main{
        padding: 0px;
        border: 2px solid #d7dde4;
        border-radius: 5px;
    }
    .olay-content-header{
        border-radius: 2px;
        height: 300px;
        background-image: url(https://i.loli.net/2017/12/16/5a34103a09385.jpeg);
        background-repeat: no-repeat;
        margin-bottom: 100px;
    }
    .olay-content-header img{
        width: 230px;
        height: 230px;
        border-radius: 230px;
        border: 15px solid #fff;
        margin-top: 180px;
        margin-left: 400px;
    }
    .olay-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .other-info{
        margin: 10px 50px;
    }
    .other-info p{
        font-size: 17px;
        word-break:break-all;
        word-wrap:break-word;
    }
    .other-info strong{
        color: #9ea7b4;
    }
</style>
