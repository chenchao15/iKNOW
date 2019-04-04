<template>
  <div>
    <Table border :columns="team_columns" :data="team_datas"></Table>
    <Modal v-model="handoverflag" width="300" @on-ok="ishandover">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>移交队长</span>
      </p>
      <p style="text-align:center">
        <span>您确定要<strong>移交队长</strong>吗？</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <span>如果移交队长，您将没有队长特权</span>
      </p>
      <Input v-model="handoverplayer" placeholder="请输入移交的队员姓名…"></Input>
      <Input v-model="handovercontent" type="textarea" :autosize="{minRows: 2,maxRows: 6}" placeholder="请输入移交原因…"></Input>
    </Modal>
    <Modal v-model="punishflag" width="300">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>处分队员</span>
      </p>
      <div style="text-align: center">
        <Button type="primary" @click="warn">警告</Button>
        <Button type="primary" @click="kickout">踢出</Button>
      </div>
      <div slot="footer" style="text-align: right">
        <Button type="ghost" @click="cancelPunish">取消</Button>
      </div>
    </Modal>
    <Modal v-model="warnflag" width="300" @on-ok="iswarn">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>警告队员</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <span>警告队员：{{punishname}}</span>
      </p>
      <Input v-model="warncontent" type="textarea" :autosize="{minRows: 2,maxRows: 6}" placeholder="请输入警告内容…"></Input>
    </Modal>
    <Modal v-model="dissolveflag" width="300" @on-ok="isdissolve">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>解散队伍</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <span>您确定要解散队伍吗？</span>
      </p>
      <Input v-model="dissolvecontent" type="textarea" :autosize="{minRows: 2,maxRows: 6}" placeholder="请输入解散原因…"></Input>
    </Modal>
    <Modal v-model="applyflag" width="300" @on-ok="isapply">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>申请队长</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <span>您确定要申请队长吗？</span>
      </p>
      <Input v-model="applycontent" type="textarea" :autosize="{minRows: 2,maxRows: 6}" placeholder="请输入申请队长原因…"></Input>
    </Modal>
    <Modal v-model="quitflag" width="300" @on-ok="isquit">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>退出队伍</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <span>您确定要退出队伍吗？</span>
      </p>
      <Input v-model="quitcontent" type="textarea" :autosize="{minRows: 2,maxRows: 6}" placeholder="请输入退出队伍原因…"></Input>
    </Modal>
    <Modal v-model="codeflag" width="300" @on-ok="iscode">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>生成加入码</span>
      </p>
      <Input v-model="codecontent" type="textarea" :autosize="{minRows: 2,maxRows: 6}" placeholder="加入码…"></Input>
    </Modal>
  </div>
</template>
<script>

export default {
  name: 'teamManage',
  props: ['stageId'],
  data () {
    return {
      codeflag: false,
      codecontent: null,
      applyflag: false,
      applycontent: null,
      quitflag: false,
      quitcontent: null,
      dissolveflag: false,
      dissolvecontent: null,
      handoverflag: false,
      handoverplayer: null,
      handovercontent: null,
      punishflag: false,
      punishindex: null,
      punishname: null,
      warnflag: false,
      warncontent: null,
      team_player: {name: '', identity: ''},
      team_id: 0,
      team_columns: [
        {
          type: 'index',
          width: 60,
          align: 'center'
        },
        {
          title: '姓名',
          key: 'name',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '身份',
          key: 'identity',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '操作',
          key: 'action',
          width: 330,
          align: 'center',
          render: (h, params) => {
            if (this.team_player.identity === '队长') {
              if (this.team_player.name === this.team_datas[params.index].name) {
                return h('div', [
                  h('Button', {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.show(params.index)
                      }
                    }
                  }, '队长信息'),
                  h('Button', {
                    props: {
                      type: 'success',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.handover(params.index)
                      }
                    }
                  }, '移交队长'),
                  h('Button', {
                    props: {
                      type: 'info',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.invitationCode(params.index)
                      }
                    }
                  }, '生成加入码'),
                  h('Button', {
                    props: {
                      type: 'error',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.dissolve(params.index)
                      }
                    }
                  }, '解散队伍')
                ])
              } else {
                return h('div', [
                  h('Button', {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.show(params.index)
                      }
                    }
                  }, '队员信息'),
                  h('Button', {
                    props: {
                      type: 'info',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.contact(params.index)
                      }
                    }
                  }, '联系队员'),
                  h('Button', {
                    props: {
                      type: 'error',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.punishindex = params.index
                        this.punishname = this.team_datas[params.index].name
                        this.punish(params.index)
                      }
                    }
                  }, '处分队员')
                ])
              }
            } else {
              if (this.team_datas[params.index].name === this.team_player.name) {
                return h('div', [
                  h('Button', {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.show(params.index)
                      }
                    }
                  }, '队员信息'),
                  h('Button', {
                    props: {
                      type: 'success',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.apply(params.index)
                      }
                    }
                  }, '申请队长'),
                  h('Button', {
                    props: {
                      type: 'error',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.quit(params.index)
                      }
                    }
                  }, '申请退队')
                ])
              } else if (this.team_datas[params.index].identity === '队长') {
                return h('div', [
                  h('Button', {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.show(params.index)
                      }
                    }
                  }, '队长信息'),
                  h('Button', {
                    props: {
                      type: 'info',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.contact(params.index)
                      }
                    }
                  }, '联系队长')
                ])
              } else {
                return h('div', [
                  h('Button', {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      marginRight: '5px'
                    },
                    on: {
                      click: () => {
                        this.show(params.index)
                      }
                    }
                  }, '队员信息'),
                  h('Button', {
                    props: {
                      type: 'info',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.contact(params.index)
                      }
                    }
                  }, '联系队员')
                ])
              }
            }
          }
        }
      ],
      team_datas: []
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/team_detail', {params: { phase_id: this.stageId }})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.team_id = res.team_id
        this.team_player = res.team_player
        this.team_datas = res.team_datas
      })
      .catch((response) => {
        this.$Message.error('您不处于任何小组')
        this.team_datas = []
      })
    },
    show (index) {
      this.$Modal.info({
        title: '个人信息',
        content: `姓名：${this.team_datas[index].name}<br>身份：${this.team_datas[index].identity}`
      })
    },
    invitationCode (index) {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/invitation_code', {params: { team_id: this.team_id }})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.codecontent = res.invitation_code
        this.codeflag = true
      })
      .catch((response) => {
        this.$Modal.error({
          title: '生成加入码失败',
          content: `您已用完所有加入码`
        })
        this.codeflag = false
        this.codecontent = null
      })
    },
    iscode () {
      this.codeflag = false
      this.codecontent = null
    },
    contact (index) {
      var type = 0
      var id = this.team_datas[index].id
      var mid = this.team_datas[index].uid
      this.$router.push('/otherUserPage/' + mid + '/' + id + '/' + type)
    },
    punish (index) {
      this.punishflag = true
    },
    cancelPunish () {
      this.punishflag = false
    },
    warn () {
      this.punishflag = false
      this.warnflag = true
    },
    iswarn () {
      this.warnflag = false
      this.$Notice.success({
        title: '警告已发出',
        desc: `“${this.team_datas[this.punishindex].name}”成员已被您警告<br>警告内容：${this.warncontent}`
      })
    },
    kickout () {
      this.punishflag = false
      this.$Modal.confirm({
        title: '踢出队伍',
        content: `您确定要将该名成员踢出队伍吗？<br>姓名：${this.team_datas[this.punishindex].name}<br>身份：${this.team_datas[this.punishindex].identity}`,
        onOk: () => {
          this.team_datas.splice(this.punishindex, 1)
          this.$Notice.success({
            title: '踢出成功',
            desc: `姓名：${this.team_datas[this.punishindex].name}<br>身份：${this.team_datas[this.punishindex].identity}<br>该名成员已被您踢出队伍`
          })
        }
      })
    },
    dissolve (index) {
      this.dissolveflag = true
    },
    isdissolve () {
      this.dissolveflag = false
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', {phase_id: this.stageId, event_type: 5, content: this.dissolvecontent, is_team: 1})
      .then((response) => {
        this.$Notice.success({
          title: '申请解散队伍审核中',
          desc: `申请解散队伍请求已发出，等待审核……`
        })
      })
      .catch((response) => {
        this.$Notice.error({
          title: '申请解散队伍请求失败',
          desc: `解散队伍请求失败……`
        })
      })
    },
    handover (index) {
      this.handoverflag = true
    },
    ishandover () {
      this.handoverflag = false
      var flag = false
      if (this.handoverplayer === this.team_player.name) {
        this.$Notice.success({
          title: '移交队长失败',
          desc: `他已经是该队伍的队长了，请重新操作`
        })
      } else {
        var handoverId = 0
        for (var i in this.team_datas) {
          if (this.team_datas[i].name === this.handoverplayer) {
            flag = true
            handoverId = this.team_datas[i].id
            break
          }
        }
        if (flag) {
          this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', {phase_id: this.stageId, event_type: 4, content: this.handovercontent, is_team: handoverId})
          .then((response) => {
            this.$Notice.success({
              title: '申请移交队长审核中',
              desc: `申请移交队长请求已发出，等待审核……`
            })
          })
          .catch((response) => {
            this.$Notice.error({
              title: '申请移交队长请求失败',
              desc: `申请移交队长请求失败……`
            })
          })
        } else {
          this.$Notice.success({
            title: '移交队长失败',
            desc: `该队伍内没有名字叫“${this.handoverplayer}”的成员，请重新操作`
          })
        }
      }
    },
    apply (index) {
      this.applyflag = true
    },
    isapply () {
      this.applyflag = false
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', {phase_id: this.stageId, event_type: 5, content: this.applycontent, is_team: 1})
      .then((response) => {
        this.$Notice.success({
          title: '申请队长审核中',
          desc: `申请队长请求已发出，等待审核……`
        })
      })
      .catch((response) => {
        this.$Notice.error({
          title: '申请队长请求失败',
          desc: `申请队长请求失败……`
        })
      })
    },
    quit (index) {
      this.quitflag = true
    },
    isquit () {
      this.quitflag = false
      this.$Modal.confirm({
        title: '申请退队',
        content: `您确定要退出队伍吗？`,
        onOk: () => {
          this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', {phase_id: this.stageId, event_type: 2, content: this.quitcontent, is_team: 1})
          .then((response) => {
            this.$Notice.success({
              title: '申请退队审核中',
              desc: `申请退队请求已发出，等待审核……`
            })
          })
          .catch((response) => {
            this.$Notice.error({
              title: '申请退队请求失败',
              desc: `退队请求失败……`
            })
          })
        }
      })
    }
  }
}
</script>
<style scoped>
</style>