<template>
  <div>
    <div class="card-header">
      <div class="card-header-title">
        What do the colours mean?
      </div>
      <div class="card-header-icon">
        <a class="icon" @click="() => { this.$emit('close') }">
          <i class="material-icons">close</i>
        </a>
      </div>
    </div>
    <div class="card-content">
      <p>Please note that all references to a "Maximum Item Level" (Max IL) refer to the Item Level of the Weapon obtained from the Tier's final raid.</p>
      <p>For example, the Max IL for Pandæmonium: Asphodelos is 605.</p>
      <hr />
      <table class="table is-bordered is-fullwidth gear-table" :class="[`is-${$store.state.user.theme}`]">
        <tr>
          <th class="is-il-bis">Best in Slot</th>
        </tr>
        <tr>
          <th class="is-il-minus-0">Max IL Gear that is not Best in Slot</th>
        </tr>
        <tr>
          <th class="is-il-minus-5">Max IL - 5 (Typically Augmented Tome Gear)</th>
        </tr>
        <tr>
          <th class="is-il-minus-10">Max IL - 10 (Typically Later Trial Weapon)</th>
        </tr>
        <tr>
          <th class="is-il-minus-15">Max IL - 15 (Typically Unaugmented Tome Gear)</th>
        </tr>
        <tr>
          <th class="is-il-minus-20">Max IL - 20 (Typically Early Catchup Trial Weapon)</th>
        </tr>
        <tr>
          <th class="is-il-minus-25">Max IL - 25 (Typically Crafted Sets)</th>
        </tr>
        <tr>
          <th class="is-il-out-of-range">Out of the range of the Team's current Tier</th>
        </tr>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Legend extends Vue {}
</script>
