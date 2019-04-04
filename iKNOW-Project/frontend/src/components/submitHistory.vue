<template>
  <div>
    <Table border :columns="columns" :data="datas"></Table>
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
  name: 'submitHistory',
  props: ['stageId'],
  data () {
    return {
      downloadflag: false,
      downloadcontent: null,
      columns: [
        {
          title: '提交时间',
          key: 'time',
          align: 'center',
          sortable: 'true',
          ellipsis: 'true'
        },
        {
          title: '批改状态',
          key: 'status',
          align: 'center',
          render: (h, params) => {
            const row = params.row
            const color = row.is_handled === 1 ? 'green' : row.is_handled === 0 ? 'red' : 'black'
            const text = row.is_handled === 1 ? '已批改' : row.is_handled === 0 ? '未批改' : 'default'
            return h('strong', {
              style: {
                color: color
              }
            }, text)
          }
        },
        {
          title: '得分',
          key: 'submit_grade',
          align: 'center',
          sortable: 'true',
          ellipsis: 'true'
        },
        {
          title: '操作',
          key: 'action',
          width: 100,
          align: 'center',
          render: (h, params) => {
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
              }, '试卷下载')
            ])
          }
        }
      ],
      datas: []
    }
  },
  mounted () {
    this.$http.get(this.GLOBAL.baseUrl + 'api/competition/submit_history', {params: { phase_id: this.stageId }})
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      this.datas = res
    })
    .catch((response) => {
      this.$Message.error('获取提交历史失败')
      this.datas = []
    })
  },
  methods: {
    download (index) {
      this.downloadflag = true
      this.downloadcontent = this.datas[index].submit_url
    }
  }
}
</script>
<style scoped>
</style>