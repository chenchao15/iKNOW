<template>
  <div>
    <Card>
      <Row>
        <p class="check-title">
          资料
        </p>
      </Row>
      <Row class="card-content upload-card">
          <div>
            <Form :label-width="100">
              <Row v-for="(down, index) in DownloadItem" :key="down.name">
                <FormItem :label="down.name" prop="name">
                  <a :href="down.attachment_url" class="TestUpload-p" >{{ down.attachment_url }}</a>
                </FormItem>
              </Row>
            </Form>
          </div>
      </Row>
    </Card>
  </div>
</template>

<script>
export default {
  name: 'materialDownload',
  props: ['stageId'],
  data () {
    return {
      DownloadItem: []
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {       // 通过this.stageId获取下载试卷格式DownloadItem
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/list_attachment?id=' + this.$route.params.id)
      .then((response) => {
        var res0 = JSON.parse(response.bodyText)
            /*
            [
                {
                    "attachment_url": "static/static/attachment/test_1514834601.docx",
                    "competition": 4,
                    "id": 2,
                    "islook": "所有人(包括游客)",
                    "label": "999",
                    "name": "0999"
                }
            ]
            */
        this.DownloadItem = res0
        for (var i in this.DownloadItem) {
          this.DownloadItem[i].attachment_url = this.GLOBAL.baseUrl + this.DownloadItem[i].attachment_url
        }
      }).catch((response) => {
        this.DownloadItem = []
        this.$Message.error('失败')
      })
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
