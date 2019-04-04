<template>
<div class="primsg">
  <h1>私信</h1>
  <Card class="card-card" v-for="(primsg, index) in primsgs" :key="primsg.name">
    <Row>
      <Col span="3">
        <Button size="small" type="text" @click="showAvatar(primsg, index)">
          <Badge :count="primsg.content.isread">
            <img style="width:40px; height:40px; border-radius: 100px;" :src="primsg.picurl"/>
          </Badge>
        </Button>
      </Col>
      <Col span="21">
        <Row>
          <Col span="8">
            <p class="card-title" v-if="primsg.author.contestant_user !== null">{{primsg.author.contestant_user.name}}</p>
            <p class="card-title" v-if="primsg.author.organizer_user !== null">{{primsg.author.organizer_user.name}}</p>
          </Col>
          <Col span="1" offset="13">
            <Button class="card-buttonone" size="large" type="text" @click="linkGoChat(primsg, index)">私信<Icon type="paper-airplane"></Icon></Button>
          </Col>
        </Row>
        <p class="card-p" v-if="primsg.content.isother === 1">
          对方:{{primsg.content.content}}
        </p>
        <p class="card-p" v-else>
          我:{{primsg.content.content}}
        </p>
      </Col>
    </Row>
  </Card>
  <div>
    <Modal v-model="msgModal" width="800" @on-visible-change="modalChange">
      <p slot="header" style="color:#5cadff;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>发送私信</span>
      </p>
      <Card class="card-card">
        <Row>
          <Col span="30">
            <Row>
              <Col span="2">
                <Button size="small" type="text" @click="goPripage"><Avatar style="width:35px; height:35px; border-radius: 70px; margin-top: -10px" :src="modalMsg.picurl" @click="goChat"/></Button>
              </Col>
              <Col span="8">
                <p class="card-title">{{modalMsg.name}}</p>
              </Col>
              <Col span="2" offset="10">
                <Button class="card-buttonone" type="text" @click="getAllMsg(modalMsg.contents)" v-if="isTalkList===false">聊天记录<Icon type="chatbubble-working"></Icon></Button>
                <Button class="card-buttonone" type="text" @click="returnMsg" v-else>发送消息<Icon type="paper-airplane"></Icon></Button>
              </Col>
            </Row>
            <div class="card-p">
              <p v-if="modalMsg.contents[modalMsg.contents.length-1].isother === 1">
               {{modalMsg.name}}:{{modalMsg.contents[modalMsg.contents.length-1].content}}
              </p>
              <p v-else>
                我:{{modalMsg.contents[modalMsg.contents.length-1].content}}
              </p>
            </div>
          </Col>
        </Row>
      </Card>
      <div class="card-modal" v-if="this.isTalkList === false">
        <p class="card-modal-p">发私信给{{modalMsg.name}}</p>
        <Input class="card-modal-input" v-model="myMsg" type="textarea" :autosize="{minRows: 6,maxRows: 10}" placeholder="请输入要发送的信息．．．"></Input>
      </div>
      <div class="card-modal" v-if="this.isTalkList === true">
        <Table height="300" :columns="columns1" :data="data2"></Table>
      </div>
      <div slot="footer">
        <Button type="info" size="large" long :loading="modalLoading" @click="linkSendMsg">发送</Button>
      </div>
    </Modal>
    <Modal title="他/她的头像" v-model="picModal" width="600">
      <div class="modal-image">
        <img :src="image" style="width:100%;height:600px">
        <div class="modal-image-cover">
          <p type="text" class="modal-image-p" @click="toOtherPage()">来看看Ta的空间吧</p>
        </div>
      </div>
      <div slot="footer">
      </div>
    </Modal>
  </div>
</div>
</template>

<script>
export default {
  name: 'primsg',
  data () {
    return {
      msgModal: false,
      modalLoading: false,
      isTalkList: false,
      primsgs: [],
      index: -1,
      picModal: false,
      image: '',
      modalMsg: {
        'id': 0,
        'name': '',
        'picurl': '',
        'contents': [
          {isother: 0, content: ''}
        ]
      },
      myMsg: '',
      columns1: [
        {
          title: '聊天记录',
          key: 'content',
          render: (h, params) => {
            if (params.row.isother === 0) {
              return h('div', {
                style: {
                  marginLeft: '300px',
                  width: '400px'
                }
              },
                [
                  h('Avatar', {
                    props: {
                      src: params.row.avatar
                    },
                    style: {
                      float: 'right'
                    }
                  }),
                  h('strong', {
                    style: {
                      float: 'right',
                      marginTop: '5px',
                      marginRight: '10px'
                    }
                  },
                    params.row.content)
                ])
            } else {
              return h('div', {
                style: {
                  width: '400px'
                }
              }, [
                h('Avatar', {
                  props: {
                    src: params.row.avatar
                  }
                }),
                h('strong', {
                  style: {
                    marginLeft: '10px'
                  }
                },
                  params.row.content)
              ])
            }
          }
        }
      ],
      data2: [
      ]
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/personal_letter')
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.primsgs = res.receivers
      })
      .catch((response) => {
        this.$Message.error('获取私信失败')
        this.primsgs = []
      })
    },
    linkSendMsg () {
      this.modalLoading = true
      setTimeout(() => {
        this.modalLoading = false
        this.msgModal = false
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/personal_letter', {id: this.modalMsg.id, content: this.myMsg})
        .then((response) => {
          this.$Message.success('发送私信成功')
        })
        .catch((response) => {
          this.$Message.error('发送私信失败')
        })
        this.myMsg = ''
      }, 1500)
    },
    linkGoChat (msg, index) {
      this.primsgs[index].content.isread = 0
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/letter_detail', {params: { id: msg.author.id }})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.modalMsg.contents = res.our_letters
      })
      .catch((response) => {
        this.$Message.error('获取私信失败')
        this.modalMsg.contents = []
      })
      this.modalMsg.id = msg.author.id
      if (msg.author.contestant_user !== null) {
        this.modalMsg.name = msg.author.contestant_user.name
      } else if (msg.author.organizer_user !== null) {
        this.modalMsg.name = msg.author.organizer_user.name
      }
      this.modalMsg.picurl = msg.picurl
      this.msgModal = true
      this.isTalkList = false
    },
    showAvatar (primsg, index) {
      this.image = primsg.picurl
      this.index = index
      this.picModal = true
    },
    getAllMsg (contents) {
      var len = contents.length
      var index
      var str = {
        avatar: '',
        content: '',
        isother: 0
      }
      for (index = 0; index < len; index++) {
        str.content = contents[index].content
        str.isother = contents[index].isother
        if (contents[index].isother === 1) {
          str.avatar = this.modalMsg.picurl
        } else {
          str.avatar = this.GLOBAL.avatarUrl
        }
        this.data2.push({avatar: str.avatar, content: str.content, isother: str.isother})
      }
      this.isTalkList = true
    },
    returnMsg () {
      this.isTalkList = false
      this.data2.splice(0, this.data2.length)
    },
    modalChange () {
      this.data2.splice(0, this.data2.length)
    },
    toOtherPage () {
      var user = this.primsgs[this.index].author
      var mid = user.id
      if (user.organizer_user !== null) {
        this.$router.push('/otherUserPage/' + mid + '/' + user.organizer_user.id + '/1')
      } else if (user.contestant_user !== null) {
        this.$router.push('/otherUserPage/' + mid + '/' + user.contestant_user.id + '/0')
      }
      this.picModal = false
    }
  }
}
</script>

<style scoped>
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
    .card-p{
        font-size: 14px;
        color: #aaa;
        line-height: 23px;
        position: relative;
    }
    .card-buttonone{
        padding:0;
        font-size: 15px;
    }
    .card-modal{
        padding: 0 20px;
    }
    .card-modal-p{
        font-size: 17px;
        font-weight: bold;
        margin-top: 10px;
        color: #80848f;
    }
    .card-modal-inpput{
        margin-left: 20px;
        margin-right: 20px;
    }
    .modal-image{
    }
    .modal-image-cover{
        display: none;
        position: absolute;
        top: 67px;
        width: 568px;
        height: 600px;
        background: rgba(0,0,0,.4);
    }
    .modal-image:hover .modal-image-cover{
        display: block;
    }
    .modal-image-p{
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        color: #f8f8f9;
        cursor: pointer;
        margin-top: 200px;
    }
</style>
