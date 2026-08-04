/*
    NotesSection

    Allows the user to enter any notes
    about the day.
*/

import TextArea from "../../../components/TextArea";

function NotesSection() {
  return (
    <section>

      {/* Section Heading */}
      <h2>Notes</h2>

      <TextArea
        label="Notes"
        id="notes"
        name="notes"
        rows={6}
        placeholder="Enter any notes for today"
      />

    </section>
  );
}

export default NotesSection;