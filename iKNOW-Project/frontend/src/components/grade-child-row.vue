<template>
  <div class="expand-row">
    <Table :columns="tableColumns" :data="tableData"></Table>
    <Modal v-model="modifyflag" width="300" @on-ok="ismodify" style="text-align:center;">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>修改成绩</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <span>原成绩：{{modifygrade}}</span>
      </p>
      新成绩：
      <InputNumber v-model="modifycontent" :min="0" style="width:100px"></InputNumber>
    </Modal>
    <Modal v-model="downloadflag" width="300" style="text-align:center;">
      <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
        <Icon type="information-circled"></Icon>
        <span>下载试卷</span>
      </p>
      <p style="margin-bottom:10px; text-align:center">
        <a :href="downloadcontent" download>{{downloadcontent}}</a>
      </p>
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
      downloadflag: false,
      downloadcontent: null,
      modifyflag: false,
      modifycontent: 0,
      modifyindex: null,
      modifygrade: null,
      tableData: [],
      tableColumns: [
        {
          title: '提交成绩',
          key: 'submit_grade',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '提交时间',
          key: 'time',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '操作',
          key: 'action',
          width: 250,
          align: 'center',
          render: (h, params) => {
            if (this.competitionType === '个人赛') {
              return h('div', [
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
                      this.download(params.index)
                    }
                  }
                }, '试卷下载'),
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
                }, '成绩信息'),
                h('Button', {
                  props: {
                    type: 'success',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.modifyindex = params.index
                      this.modifygrade = this.tableData[params.index].submit_grade
                      this.gradeModify(params.index)
                    }
                  }
                }, '成绩修改')
              ])
            } else {
              return h('div', [
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
                      this.download(params.index)
                    }
                  }
                }, '试卷下载'),
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
                }, '成绩信息'),
                h('Button', {
                  props: {
                    type: 'success',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.modifyindex = params.index
                      this.modifygrade = this.tableData[params.index].submit_grade
                      this.gradeModify(params.index)
                    }
                  }
                }, '成绩修改')
              ])
            }
          }
        }
      ]
    }
  },
  mounted () {
    this.tableData = this.row.grades
  },
  methods: {
    download (index) {
      this.downloadflag = true
      this.downloadcontent = this.tableData[index].submit_url
    },
    show (index) {
      this.$Modal.info({
        title: '成绩信息',
        content: `成绩：${this.tableData[index].submit_grade}<br>提交时间：${this.tableData[index].time}`
      })
    },
    gradeModify (index) {
      this.modifyflag = true
    },
    ismodify () {          // post给后端新修改的成绩
      this.modifyflag = false
      var dataPost = {
        grade_id: this.tableData[this.modifyindex].id,
        submit_grade: this.modifycontent
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/handle_grade', dataPost)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.tableData[this.modifyindex].is_handled = 1
          this.tableData[this.modifyindex].submit_grade = res.submit_grade
          this.$Notice.success({
            title: '成绩已修改',
            desc: `该成绩已被您修改<br>原成绩：${this.modifygrade}<br>修改后成绩：${this.modifycontent}`
          })
        })
        .catch((response) => {
          this.$Message.error('成绩修改失败')
        })
    },
    formatDate (date) {
      const y = date.getFullYear()
      let m = date.getMonth() + 1
      m = m < 10 ? '0' + m : m
      let d = date.getDate()
      d = d < 10 ? ('0' + d) : d
      return y + '-' + m + '-' + d
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