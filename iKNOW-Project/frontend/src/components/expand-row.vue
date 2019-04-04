<style>
</style>
<template>
  <div>
    <Row>
      <Col span="8" offset="9">
        <a :href="row.attachment_url" :download="row.name">附件下载地址：{{ row.name }}</a>
      </Col>
      <Col span="5" offset="1">
        <Button type="error" @click="deleteFilePost">删除附件</Button>
      </Col>
    </Row>
  </div>
</template>
<script>
export default {
  props: {
    row: Object
  },
  methods: {
    deleteFilePost () {
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/delete_attachment', {id: this.row.id})
      .then((response) => {
        this.$Message.success('删除成功')
      })
      .catch((response) => {
        this.$Message.error('删除失败')
      })
    }
  }
}
</script>
