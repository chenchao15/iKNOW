<template>
  <div class="expand-row">
    <Table :columns="tableColumns" :data="tableData"></Table> <!-- :show-header="false"-->
    <Modal v-model="punishflag" width="300">
        <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
          <Icon type="information-circled"></Icon>
          <span>队员处置</span>
        </p>
        <div style="text-align: center">
          <Button type="primary" @click="warn">警告</Button>
          <!--<Button type="primary" @click="kickout">踢出</Button>-->
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
  </div>
</template>

<script>
export default {
  props: {
    row: Object
  },
  data () {
    return {
      punishflag: false,
      warnflag: false,
      punishindex: null,
      punishname: null,
      warncontent: null,
      tableColumns: [
        {
          title: '姓名',
          key: 'name',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '选手身份',
          key: 'identity',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '操作',
          key: 'action',
          width: 250,
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
              }, '队员信息'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.punishindex = params.index
                    this.punishname = this.tableData[params.index].name
                    this.punish(params.index)
                  }
                }
              }, '队员处置')
            ])
          }
        }
      ],
      tableData: [],
      stageId: null
    }
  },
  mounted () {
    this.tableData = this.row.team_member
    this.stageId = this.row.stage_id
  },
  methods: {
    show (index) {
      this.$Modal.info({
        title: '队员信息',
        content: `姓名：${this.tableData[index].name}<br>身份：${this.tableData[index].identity}`
      })
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
      var dataPost = {
        phase_id: this.stageId,
        contestant_id: this.tableData[this.punishindex].id,
        event_type: 7,
        is_team: 1,
        content: this.warncontent
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', dataPost)
      .then((response) => {
        this.$Notice.success({
          title: '警告已发出',
          desc: `“${this.tableData[this.punishindex].name}”成员已被您警告<br>警告内容：${this.warncontent}`
        })
      })
      .catch((response) => {
        this.$Message.error('发送警告失败')
      })
    }
  }
}
</script>

<style scoped>
  .expand-row{
    padding: 0px;
    margin: 0px -51px; /*-24*/
    background: white;
  }
</style>