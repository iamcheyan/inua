package assistantui

import (
	"reflect"
	"testing"
)

func TestEnqueuePromptPreservesOrderAndTrims(t *testing.T) {
	pending := enqueuePrompt(nil, "  first question  ")
	pending = enqueuePrompt(pending, "\t\n")
	pending = enqueuePrompt(pending, "second question")
	if want := []string{"first question", "second question"}; !reflect.DeepEqual(pending, want) {
		t.Fatalf("queued prompts = %#v, want %#v", pending, want)
	}
}
