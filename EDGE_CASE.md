# Document your edge case here

- To get marks for this section you will need to explain to your tutor:

1. The edge case you identified
2. How you have accounted for this in your implementation

- Edge case identified: **What happens if a student has been deleted from the db, but they are present on the frontend?**
- How I have accounted for this: When a student is deleted from the db, the frontend will attempt to fetch the student details when the user clicks on the student card. If the student has been deleted, the backend will return a 404 error, which the frontend will handle by displaying an error message to the user.

- Edge case identified: **What happens to stats if mark is updated or a student is deleted**
- How I have accounted for this: Eric's frontend implementation would only fetch stats on initial load, so if a student is updated or deleted, the stats would not be updated. To account for this, I have added a `refreshKey` prop to the `Stats` component, which is updated whenever a student is created, updated, or deleted. This will trigger the `useEffect` hook in the `Stats` component to refetch the stats from the backend and update the displayed stats accordingly.
