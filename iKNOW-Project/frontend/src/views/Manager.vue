<template>
  <div>
    <managerBar></managerBar>
    <div style="margin-top: 50px">
      <managerHandle></managerHandle>
    </div>
  </div>
</template>
<script>
import managerBar from '../components/managerBar'
import managerHandle from '../components/managerHandle'
export default {
  name: 'manager',
  data () {
    return {
    }
  },
  components: {
    managerBar,
    managerHandle
  },
  methods: {
  }
}
</script>

<style>
</style>
