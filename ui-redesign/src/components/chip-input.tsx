"use client";

import { X } from "lucide-react";
import { KeyboardEvent, useState } from "react";

type ChipInputProps = {
  label: string;
  values: string[];
  onChange: (values: string[]) => void;
  placeholder?: string;
  helper?: string;
};

export function ChipInput({ label, values, onChange, placeholder, helper }: ChipInputProps) {
  const [draft, setDraft] = useState("");

  function pushValue(nextValue: string) {
    const cleaned = nextValue.trim();
    if (!cleaned || values.includes(cleaned)) {
      return;
    }
    onChange([...values, cleaned]);
    setDraft("");
  }

  function handleKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === "Enter" || event.key === ",") {
      event.preventDefault();
      pushValue(draft);
    }

    if (event.key === "Backspace" && !draft && values.length) {
      onChange(values.slice(0, -1));
    }
  }

  return (
    <div className="field-group">
      <label className="field-label">{label}</label>
      <div className="chip-box">
        {values.map((value) => (
          <button key={value} type="button" className="chip" onClick={() => onChange(values.filter((item) => item !== value))}>
            {value}
            <X size={14} />
          </button>
        ))}
        <input
          className="chip-input"
          value={draft}
          placeholder={placeholder ?? "Type and press Enter"}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={() => pushValue(draft)}
        />
      </div>
      {helper ? <p className="field-helper">{helper}</p> : null}
    </div>
  );
}