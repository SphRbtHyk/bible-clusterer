<template>
  <b-col>
    <b-form-group>
      <template #label>
        <b-form-checkbox
          v-model="allSelected"
          :indeterminate="indeterminate"
          aria-describedby="booklist"
          aria-controls="booklist"
          @change="toggleAll"
          switch
        >
          {{ allSelected ? bookgroup : bookgroup }}
        </b-form-checkbox>
      </template>

      <template v-slot="{ ariaDescribedby }">
        <b-form-checkbox-group
          :id="bookgroup"
          v-model="selected"
          :options="booklist"
          :aria-describedby="ariaDescribedby"
          name="booklist"
          class="ml-4"
          aria-label="Individual booklist"
          stacked
        ></b-form-checkbox-group>
      </template>
    </b-form-group>

    <!-- <div>
      Selected: <strong>{{ selected }}</strong
      ><br />
      All Selected: <strong>{{ allSelected }}</strong
      ><br />
      Indeterminate: <strong>{{ indeterminate }}</strong>
    </div> -->
    <!-- </template> -->
  </b-col>
</template>

<script>
export default {
  name: "Checkboxes",
  props: {
    booklist: [],
    bookgroup: String,
  },
  data() {
    return {
      allSelected: false,
      indeterminate: false,
      selected: [],
    };
  },
  methods: {
    toggleAll(checked) {
      this.selected = checked ? this.booklist.slice() : [];
    },
  },
  watch: {
    selected(newValue) {
      // Handle changes in individual book checkboxes
      // Add the new value
      this.$parent.selectedGlobal[this.bookgroup] = newValue;
      if (newValue.length === 0) {
        this.indeterminate = false;
        this.allSelected = false;
      } else if (newValue.length === this.booklist.length) {
        this.indeterminate = false;
        this.allSelected = true;
        console.log(this.allSelected);
      } else {
        this.indeterminate = true;
        this.allSelected = false;
      }
    },
  },
};
</script>
