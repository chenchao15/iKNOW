<template>
  <div>
    <Card>
      <Row>
        <p class="check-title">
          试卷
        </p>
      </Row>
      <!--<Row>
        <p v-if="competitionType === '个人赛'">
          <Col span="5" offset="8">姓名：{{author.name}}</Col><Col span="7">时间：{{author.time}}</Col>
        </p>
        <p v-else-if="competitionType === '小组赛'">
          <Col span="5" offset="7">队伍：{{author.name}}</Col><Col span="5">时间：{{author.time}}</Col>
        </p>
      </Row>-->
      <Row class="card-content upload-card">
          <div>
            <Form :label-width="100">
              <Row v-for="(down, index) in DownloadItem" :key="down.name">
                <Col span="20" v-if="down.type==='singleLine' || down.type==='multiLine'">
                  <FormItem label="提示信息" prop="name">
                    <p class="TestUpload-p" style="width: 400px;word-break:break-all; word-wrap:break-word;" v-html="down.value">{{down.value}}</p>
                  </FormItem>
                </Col>
                <Col span="20" v-if="down.type==='editTest'">
                  <FormItem :label="down.name" prop="name">
                    <Input type="textarea" v-model="down.value" :autosize="{minRows: 20,maxRows: 100}"></Input>
                  </FormItem>
                </Col>
                <Col span="20" v-if="down.type==='Upload'">
                  <FormItem :label="down.name" prop="name">
                    <a :href="down.fileUrl" class="TestUpload-p" download>{{ down.fileUrl }}</a>
                    <!--<Upload
                      action="download">
                      <Button type="ghost" icon="ios-cloud-download-outline">请在此处下载试题</Button>
                     </Upload>-->
                  </FormItem>
                </Col>
              </Row>
            </Form>
          </div>
      </Row>
      <!--<Row v-if="examinationPaper.view_url !== ''" class="card-content">
        <Card>
          <p class="upload-result">
            浏览试卷：
          </p>
          <a @click="viewPaper(examinationPaper.view_url)">{{examinationPaper.view_url}}</a>
        </Card>
      </Row>
      <Row v-if="examinationPaper.download_url !== ''" class="card-content">
        <Card>
          <p class="upload-result">
            下载试卷：
          </p>
           <a @click="downloadPaper(examinationPaper.download_url)">{{examinationPaper.download_url}}</a>
        </Card>
      </Row> -->
    </Card>
    <Card class="upload-card">
      <Row class="card-footer">
        <p class="upload-result">
          提交结果：
        </p>
        <div>
          <Form :label-width="110">
            <Row v-for="(thing, index) in UploadItem" :key="thing.name">
              <Col span="20" v-if="thing.type==='singleLine' || thing.type==='multiLine'">
                <FormItem label="提示信息" prop="name">
                  <p class="TestUpload-p" style="width:400px;word-break:break-all; word-wrap:break-word;" v-html="thing.value">{{thing.value}}</p>
                </FormItem>
              </Col>
              <Col span="20" v-if="thing.type==='editTest'">
                <FormItem :label="thing.name" prop="name">
                  <Input type="textarea" v-model="thing.value" :autosize="{minRows: 20,maxRows: 100}"></Input>
                </FormItem>
              </Col>
              <Col span="20" v-if="thing.type==='submitCount'">
                <FormItem label="每天提交次数上限" prop="name">
                  <p class="TestUpload-p" v-if="thing.value === '1'">仅一次</p>
                  <p class="TestUpload-p" v-if="thing.value === '2'">两次</p>
                  <p class="TestUpload-p" v-if="thing.value === '3'">三次</p>
                  <p class="TestUpload-p" v-if="thing.value === '4'">无限制</p>
                </FormItem>
              </Col>
              <Col span="20" v-if="thing.type==='Upload'">
                <FormItem :label="thing.name" prop="name">
                  <Upload
                    type="drag"
                    :before-upload="handleUpload"
                    :action="GLOBAL.baseUrl + 'api/competition/submit_upload'">
                    <div style="padding: 20px 0">
                      <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                      <p>{{thing.value}}</p>
                    </div>
                  </Upload>
                  <div v-if="file !== null">文件: {{ file.name }} </div>
                </FormItem>
              </Col>
            </Row>
          </Form>
        </div>
        <div style="float:right">
          <Button type="primary" @click="confirmResult">确定</Button>
          <Col span="4"></Col>
          <Button type="ghost" @click="cancelResult" style="margin-left:6px">取消</Button>
        </div>
      </Row>
    </Card>
  </div>
</template>
<script>

export default {
  name: 'competitionEntry',
  props: ['stageId'],
  data () {
    return {
      UploadItem: [],
      file: [],
      DownloadItem: []
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {       // 通过this.stageId获取下载试卷格式DownloadItem和提交答案格式UploadItem
      /* var res1 = [
        {name: '提交附件', type: 'Upload', value: '请同学们注意提交截止时间'},
        {name: '', type: 'singleLine', value: '结果文件大小不得超过２G'},
        {name: '', type: 'submitCount', value: '3'}
      ]
      var res2 = [
        {name: '', type: 'singleLine', value: '请同学们在此处下载本阶段的试题'},
        {name: '大数据竞赛', type: 'Upload', value: '点击上传本阶段试题', fileUrl: 'https://baidu.com'}
      ] */
      console.log(this.stageId)
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + this.stageId)
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.UploadItem = JSON.parse(res.result_submit_method)
        this.DownloadItem = JSON.parse(res.test_upload_method)
      }).catch((response) => {
        this.UploadItem = []
        this.DownloadItem = []
      })
    },
    confirmResult () {   // 将答案post给后端
      var data = this.UploadItem
      var formData = new FormData()
      for (var index = 0; index < data.length; index++) {
        if (data[index].type === 'Upload') {
          console.log(this.file)       // 将this.file（试卷）传给后端
          formData.append('file', this.file, this.file.name)
          this.$http.post(this.GLOBAL.baseUrl + 'api/competition/submit_upload', formData)
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.$http.post(this.GLOBAL.baseUrl + 'api/competition/grade', {phase_id: this.stageId, submit_url: res.submit_url})
            .then((response) => {
              this.$Notice.success({
                title: '提交成功',
                desc: `提交成功，等待批改……`
              })
            }).catch((response) => {
              this.$Notice.error({
                title: '提交失败',
                desc: `提交失败……`
              })
            })
          }).catch((response) => {
          })
          var fileUrl = 'dddffff'
          data[index].fileUrl = fileUrl
          break
        }
      }
      console.log(data) // 将data当做字符串传给后端
    },
    cancelResult () {
    },
    handleUpload (file) {
      this.file = file
      return false
    }
  }
}
</script>
<style scoped>
  .card-row{
    margin: 20px 0;
    text-align: center;
  }
  .card-content{
    /* font-weight: bold;
    margin-left: 60px;
    margin-top:50px;
    z-index: 0; */
    margin: 10px 0;
    padding: 0;
    text-align: center;
  }
  .card-footer{
    margin-top: 20px;
    margin-left: 0px;
    text-align: center;
  }
  .playermanage-row{
    font-size: 15px;
    margin-top: 10px;
    margin-bottom:10px;
  }
  .havedata-div{
    margin: 50px 0 20px 100px;
    text-align: center;
  }
  .button-import{
    padding: 10px;
    font-size: 25px;
    text-align: center;
  }
  .candidate-style{
    margin-left: 70px;
    margin-bottom: 20px;
    text-align: center;
  }
  .check-title{
    margin-bottom: -10px;
    text-align: center;
    font-size: 20px;
    font-color: black;
    font-weight: bold;
  }
  .upload-result{
    margin-bottom: 10px;
    text-align: center;
    font-size: 17px;
    font-color: black;
    font-weight: bold;
  }
  .upload-card{
    margin-top: 20px; 
    text-align: left;
    font-weight: bold;
  }
  .TestUpload-p{
    font-weight: normal;
    font-size: 14px;
  }
</style>