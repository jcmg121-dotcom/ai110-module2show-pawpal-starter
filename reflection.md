# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

  My initial UML design was centered on a simple object model for pet care planning. I organized the system around an owner who manages one or more pets, with each pet having care tasks that are collected into a schedule. The design was meant to separate data (owner, pet, and task information) from planning logic so the scheduler could build a daily plan from those objects.

- What classes did you include, and what responsibilities did you assign to each?

  - Owner: represents the pet parent, stores basic contact and availability information, and manages the pets connected to that owner.
  - Pet: represents an individual animal, stores pet details, and links the pet to its owner and care schedule.
  - Task: represents a single care activity such as a walk, feeding, or medication, including its priority, timing, and completion status.
  - Schedule: organizes tasks for a pet and is responsible for generating and maintaining the daily or weekly care plan.

**b. Design changes**

- Did your design change during implementation?
  Yes. During implementation, I changed the design to make the relationships between classes more explicit. Instead of storing owner and pet information as simple IDs, I connected `Owner` and `Pet` directly and gave the scheduler a clear link to the owner and pet it was planning for.

- If yes, describe at least one change and why you made it.
  I also added task fields such as duration, priority, and preferred time because the initial skeleton did not capture enough information for realistic scheduling. These changes made the model easier to use and reduced the chance of logic becoming awkward later.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  My scheduler considers task time, priority, due date, pet ownership, and completion status. It uses the preferred time field to order tasks in a day-like plan, gives higher-priority tasks earlier placement, and filters tasks by pet or status when needed.
- How did you decide which constraints mattered most?
  I chose time and priority as the most important because they directly affect whether a care task can realistically be completed in a day. Pet association and status were also important for keeping tasks organized and making it easier to view only relevant items.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  One tradeoff is that the scheduler favors simple ordering over complex optimization. It does not try to solve every possible scheduling conflict perfectly; instead, it sorts tasks and warns about overlaps when two tasks are assigned to the same time.
- Why is that tradeoff reasonable for this scenario?
  This is reasonable because the app is a lightweight pet-care planner rather than a full scheduling system. A simple approach is easier to understand, easier to maintain, and still useful for a pet owner planning everyday tasks.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
