LunchUP
=======

This tool aims to take a large-ish population of people, and divide them into small groups for lunch.

The main goal is to develop a method to divide the large group into small groups which are also diverse.  Each person will have a set of attributes attached to them, and the tool will look at the attributes, and also past small groups, to come up with a set of groups which is diverse and ever changing.

## Background

The idea for this tool came from the [University of Arizona's IT Leadership Academy][itla]. During the months the Academy ran, there were monthly groups which were formed to go have lunch and discuss a topic for the following session. After the Academy was over, we all agreed that we really liked these lunches, and wanted to find a way to keep them going, even if there's no 'assignment' each month.

[itla]: https://it.arizona.edu/it-leadership-academy

## Technical Overview

What really got me interested in writing this was discussing algorithms with another ITLA attendee. He was talking about a genetic algorithm he had written to sort incoming medical students into groups. I did a little reading on genetic algorithms and decided this might be a great way to form groups for ongoing ITLA lunch meetings.

### Create a Population with Attributes

First off we need a population of people to work with, along with attributes attached to each person.

### Make Some Groups

The next step is to simply create a set of random groups.  This is pretty easy since we know the population size.

### Create a Scoring Function

This is the hardest part. We need to come up with some way of distilling the "quality" of a particular group set to a single number. You can see the code for my scoring function in `group.score_group()`, but its basically a fight between wanting to make the groups as diverse as possible (fewest number of similar attributes) and reducing the likelihood that two people will be placed into the same group as they were in last month.

During the first month or two, the 'diversity' component will dominate, and in later months with lots of history, that part seems to dominate.

This does a good job of making sure new people (with no history) get put into a group with people unlike themselves, while also doing a good job of making sure people aren't always in a group with the same people month after month.

This all gets easier with a larger population set.

### Mutations!

Once you have a scoring function, the 'genetic' fun begins! You begin with your initial random group set and give it a score. This becomes your Score To Beat. Now you randomly mutate the group set. I do this by randomly selecting two groups from the set, then randomly selecting 1 person from each group, and swap those two people. Now you have a new group set to score. If this set scores better, it becomes the group with the Score To Beat.

Repeat this process a few thousand times, and it doesn't take that long to come up with a pretty good set of groups which has the best score.

## Future Ideas

### Web interface
Initially this will just be a command line tool that is run manually.  Eventually I would like to add a customer interface for the participants to be able to register and update their preferences.

### Scheduling and Calendar Invites
Figuring out some way to pick a date for each group would be nice, as well as create iCal events and email them to each participant each month.

### Location Recommendations
Since our group seems to never be able to agree on _where_ to go, an additional aspect of this project could be having a set of lunch locations, and recommending a lunch location for the group that again tries to take into account where they've all been recently.

