<template>
  <div>
    <Table border height="600" :columns="team_columns" :data="team_datas"></Table>
    <Modal v-model="joinFlag" width="300" @on-ok="isJoinTeam">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>加入队伍</span>
      </p>
      <p style="text-align:center">
        <span>拥有<strong>队伍加入码</strong>才可以加入队伍哦～</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <span>没有的话，请联系队长索要</span>
      </p>
      <Input v-model="retrCode" placeholder="请输入队伍加入码…"></Input>
    </Modal>
  </div>
</template>
<script>

export default {
  name: 'competitionTeams',
  props: ['stageId'],
  data () {
    return {
      joinFlag: false,
      joinIndex: null,
      retrCode: null,
      competition: { title: '2017年APMCM亚太地区大学生数学建模竞赛赛', stage: '初赛', joinCodes: ['123', '456', '789', '101', '124'], id: 1 },
      team_columns: [
        {
          title: '队伍',
          key: 'team_name',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '队长',
          key: 'leader_name',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '队员人数',
          key: 'team_number',
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        },
        {
          title: '创建日期',
          key: 'create_time',
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        },
        {
          title: '操作',
          key: 'action',
          width: 200,
          align: 'center',
          render: (h, params) => {
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
              }, '详情'),
              /* h('Button', {
                props: {
                  type: 'success',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.join(params.index)
                  }
                }
              }, '加入'), */
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
          }
        }
      ],
      team_datas: []
    }
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
      console.log(this.stageId)
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/team', {params: { phase_id: this.stageId }})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.team_datas = res.team_datas
        for (var i in this.team_datas) {
          this.team_datas[i].leader_name = this.team_datas[i].team_leader.name
        }
      })
      .catch((response) => {
        /* if (response.status === 400) {
        }
        var res = JSON.parse(response.bodyText)
        this.$Message.error('获取队伍列表失败') */
        this.team_datas = []
      })
    },
    show (index) {
      this.$Modal.info({
        title: '队伍信息',
        content: `队伍名称：${this.team_datas[index].team_name}<br>队长姓名：${this.team_datas[index].leader_name}<br>队员人数：${this.team_datas[index].team_number}<br>创建时间：${this.team_datas[index].create_time}`
      })
    },
    join (index) {
      this.joinIndex = index
      this.joinFlag = true
    },
    isJoinTeam () {
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/invitation_code', {team_id: this.team_datas[this.joinIndex].team_id, invitation_code: this.retrCode})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        if (res.is_join === 1) {
          this.$Notice.success({
            title: '加入成功',
            desc: '您已成功加入该队伍，请到个人信息中心完成详细资料填写'
          })
        } else {
          this.$Notice.error({
            title: '加入失败',
            desc: '不好意思，该加入码已失效，请重新输入'
          })
        }
      })
      .catch((response) => {
        this.$Message.error('加入失败')
        this.team_datas = []
      })
      this.retrCode = null
      this.joinFlag = false
    },
    contact (index) {
      var type = 0
      var id = this.team_datas[index].team_leader.id
      var mid = this.team_datas[index].team_leader.uid
      this.$router.push('/otherUserPage/' + mid + '/' + id + '/' + type)
    }
  }
}
</script>
<style scoped>
</style>