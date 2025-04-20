<div class="calendar">
	{#each headers as header}
	    <button class="day-name">{header}</button>
	{/each}

	{#each days as day}
		{#if day.enabled}
			<button class="day" class:today={day.date.getTime() == date_today} on:click={()=>day_click_callback(day)}>
        {day.name}
        <span class="task-icons">
          {#each day.tasks as task}
          <span class="pri-icon">
            {@html get_priority_svg[Priority[task.priority]]}
          </span>
          {/each}
        </span>
      </button>
		{:else}
			<button class="day day-disabled">{day.name}</button>
		{/if}
	{/each}
</div>

<script lang="ts">
import type { CalendarDay } from "../types/CalendarDay";
import { get_priority_svg, get_today_iso } from "../store/utils";
import { Priority } from "../types/Project";

const date_today = get_today_iso()

export var headers:string[] = [];
export let days:CalendarDay[] = [];
export let day_click_callback:(_:CalendarDay) => void;
</script>

<style>
.calendar {
  display: grid;
  width: 100%;
  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: 30px;
  grid-auto-rows: 1fr;
  overflow: auto;
  gap: 8px;
}
.task-icons{
  display: block;
}
.pri-icon{
  margin-left: auto;
  display: inline-block;
  margin-right: 2px;
  width: 18px;
}
.day {
  border-bottom: 1px solid rgba(166, 168, 179, 0.12);
  border-right: 1px solid rgba(166, 168, 179, 0.12);
  text-align: right;
  padding-right: 8px;
  letter-spacing: 1px;
  font-size: 14px;
  aspect-ratio: 1/1;
  box-sizing: border-box;
  position: relative;
  font-family: inherit;
  overflow: auto;
  border: none;
  border-radius: 8px;
  font-weight: 700;
}

@media only screen and (max-width:600px){
  .day{
    text-align: center;
    font-size: 12px;
    padding-right: 0;
  }
}

.day:nth-of-type(7n + 7) {
  border-right: 0;
}
.day:nth-of-type(n + 1):nth-of-type(-n + 7) {
  grid-row: 1;
}
.day:nth-of-type(n + 8):nth-of-type(-n + 14) {
  grid-row: 2;
}
.day:nth-of-type(n + 15):nth-of-type(-n + 21) {
  grid-row: 3;
}
.day:nth-of-type(n + 22):nth-of-type(-n + 28) {
  grid-row: 4;
}
.day:nth-of-type(n + 29):nth-of-type(-n + 35) {
  grid-row: 5;
}
.day:nth-of-type(n + 36):nth-of-type(-n + 42) {
  grid-row: 6;
}
.day:nth-of-type(7n + 1) {
  grid-column: 1/1;
}
.day:nth-of-type(7n + 2) {
  grid-column: 2/2;
}
.day:nth-of-type(7n + 3) {
  grid-column: 3/3;
}
.day:nth-of-type(7n + 4) {
  grid-column: 4/4;
}
.day:nth-of-type(7n + 5) {
  grid-column: 5/5;
}
.day:nth-of-type(7n + 6) {
  grid-column: 6/6;
}
.day:nth-of-type(7n + 7) {
  grid-column: 7/7;
}
.day-name {
  font-size: 12px;
  text-transform: uppercase;
  text-align: center;
  border-bottom: 1px solid rgba(166, 168, 179, 0.12);
  font-weight: 500;
  border: none;
  background-color: var(--primary-tinted);
  border-radius: 8px;
}
.day-disabled {
  color: rgba(152, 160, 166, 0.5);
  background-color: #ffffff;
  background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23fdf9ff' fill-opacity='1' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E");
  cursor: not-allowed;
}
.today{
  background-color: var(--primary-transparent);
  border: 3px var(--primary) solid;
}
</style>
