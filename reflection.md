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

- I used my AI coding assistant throughout the project for design brainstorming, debugging, test writing, and small refactors. It was especially helpful when I wanted to turn a rough idea into working Python classes or when I needed help explaining how to structure the scheduler methods cleanly.
- The most useful prompts were specific and focused, such as asking for help refining the scheduler API, identifying edge cases for recurring tasks, or reviewing a block of code for clarity and maintainability. I also found it very helpful to ask the assistant to compare different design choices before I committed to one.

**b. Judgment and verification**

- One example of an AI suggestion I rejected was a proposal to make the scheduler do more complex automatic conflict resolution, such as shifting tasks to nearby times when a conflict was found. I modified that idea because it would have made the scheduler less transparent and less aligned with the simple, readable design I wanted for this project.
- I evaluated the AI’s suggestions by checking them against the class responsibilities in my implementation and by running the tests. If a suggestion introduced extra complexity or made the system harder to explain, I adjusted it rather than accepting it as-is.
- Using separate chat sessions for different phases helped me stay organized because I could keep design planning, implementation, and testing in distinct contexts. This made it easier to revisit earlier decisions without mixing up ideas or code changes.

---

## 4. Testing and Verification

**a. What you tested**

- I tested sorting behavior, recurring task creation, completion flow, and conflict detection for tasks that share the same preferred time.
- These tests were important because they cover the core behaviors that make the scheduler useful in real life: a schedule should be ordered clearly, recurring tasks should continue naturally, and conflicting times should be flagged instead of silently slipping through.

**b. Confidence**

- I am fairly confident that the scheduler works correctly for the core scenarios it was designed for. The tests pass and the app behavior is consistent for the main happy paths and several edge cases.
- If I had more time, I would test empty-task states, invalid or missing preferred times, very long recurring ranges, and duplicate task IDs to make the scheduler more robust.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with how the scheduler became clearer and more structured as the project evolved. The combination of tests, a simple class model, and a clean Streamlit UI made the final version feel coherent and understandable.

**b. What you would improve**

- If I had another iteration, I would improve the design by making the scheduler more flexible and adding better support for multiple pets, more advanced conflict handling, and richer task metadata.

**c. Key takeaway**

- One important lesson was that powerful AI tools are most effective when the human acts as the lead architect: setting the goals, enforcing design boundaries, and verifying the implementation. The AI can accelerate development, but the overall system still needs clear direction and thoughtful judgment.
