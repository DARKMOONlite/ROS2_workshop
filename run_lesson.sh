#!/usr/bin/env bash
set -euo pipefail

IMAGE="osrf/ros:humble-desktop"
CONTAINER_PREFIX="ros2_test"
LESSONS_DIR="lessons"

usage() {
  echo "Usage: $0 <lesson-folder> [--ro]"
  echo
  echo "Examples:"
  echo "  $0 lesson01"
  echo "  $0 lesson04 --ro"
  echo
  echo "By default, the lesson is mounted read-write. Use --ro for read-only."
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

LESSON_NAME="$1"
MODE="rw"

if [[ $# -eq 2 ]]; then
  if [[ "$2" == "--ro" ]]; then
    MODE="ro"
  else
    echo "Unknown option: $2"
    usage
    exit 1
  fi
fi

LESSON_PATH="$LESSONS_DIR/$LESSON_NAME"

if [[ ! -d "$LESSON_PATH" ]]; then
  echo "Lesson folder not found: $LESSON_PATH"
  echo
  echo "Available lessons:"
  ls -1 "$LESSONS_DIR" | sed 's/^/  - /'
  exit 1
fi

CONTAINER_NAME="${CONTAINER_PREFIX}_${LESSON_NAME}"

echo "Starting container: $CONTAINER_NAME"
echo "Mounting: $PWD/$LESSON_PATH -> /workshop/src/lesson ($MODE)"

docker run --rm -it \
  --name "$CONTAINER_NAME" \
  -v "$PWD/$LESSON_PATH:/workshop/src/lesson:$MODE" \
  -w /workshop \
  "$IMAGE"
