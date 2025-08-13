import click

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def sort_albums(file_path):
    """
    Reads a file of album names, sorts them alphabetically, and generates
    step-by-step instructions to move them to their correct sorted positions.
    """
    initial_layout = []
    shelf_capacities = []
    current_shelf_count = 0
    shelf_number = 1
    position_on_shelf = 1

    try:
        # Step 1: Read the initial state and shelf capacities
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line == '---':
                    shelf_capacities.append(current_shelf_count)
                    current_shelf_count = 0
                    shelf_number += 1
                    position_on_shelf = 1
                elif line:
                    initial_layout.append({
                        'name': line,
                        'shelf': shelf_number,
                        'pos': position_on_shelf
                    })
                    current_shelf_count += 1
                    position_on_shelf += 1
        shelf_capacities.append(current_shelf_count)

        # Step 2: Determine the final (sorted) state
        all_album_names = sorted([album['name'] for album in initial_layout])
        
        final_layout_map = {}
        current_album_index = 0
        for s_idx, capacity in enumerate(shelf_capacities, 1):
            for p_idx in range(1, capacity + 1):
                album_name = all_album_names[current_album_index]
                final_layout_map[album_name] = {'shelf': s_idx, 'pos': p_idx}
                current_album_index += 1

        # Step 3: Create a mutable representation of the current state of shelves
        live_shelves = {}
        for album in initial_layout:
            if album['shelf'] not in live_shelves:
                live_shelves[album['shelf']] = {}
            live_shelves[album['shelf']][album['pos']] = album['name']
            
        # Create a map of initial positions for easy lookup
        initial_pos_map = {album['name']: {'shelf': album['shelf'], 'pos': album['pos']} for album in initial_layout}

        # Step 4: Generate move instructions
        visited = set()
        for shelf_num in sorted(live_shelves.keys()):
            for pos_num in sorted(live_shelves[shelf_num].keys()):
                
                if (shelf_num, pos_num) in visited:
                    continue

                current_album_name = live_shelves[shelf_num][pos_num]
                target_pos = final_layout_map[current_album_name]

                # If album is already in the correct place
                if target_pos['shelf'] == shelf_num and target_pos['pos'] == pos_num:
                    click.echo(f'"{current_album_name}" on shelf {shelf_num} position {pos_num} is already in the correct location.')
                    visited.add((shelf_num, pos_num))
                    continue

                # Start a move cycle
                # The librarian is "holding" the album from the starting empty slot
                held_album = current_album_name
                
                # Find where the held album came from initially to start the instruction
                original_pos = initial_pos_map[held_album]
                click.echo(f'Take "{held_album}" from shelf {original_pos["shelf"]} position {original_pos["pos"]}.', nl=False)

                # This loop follows the chain of swaps
                while True:
                    target_for_held = final_layout_map[held_album]
                    target_shelf = target_for_held['shelf']
                    target_pos_num = target_for_held['pos']

                    # The album currently in the spot where we want to place the held album
                    displaced_album = live_shelves[target_shelf][target_pos_num]

                    click.echo(f' Replace "{displaced_album}" on shelf {target_shelf} position {target_pos_num} with "{held_album}".')
                    
                    # Update the live state
                    live_shelves[target_shelf][target_pos_num] = held_album
                    visited.add((target_shelf, target_pos_num))

                    # The librarian is now holding the displaced album
                    held_album = displaced_album

                    # If the newly held album belongs in the original empty slot, the cycle is complete
                    if final_layout_map[held_album]['shelf'] == shelf_num and final_layout_map[held_album]['pos'] == pos_num:
                        click.echo(f'Replace the now empty spot on shelf {shelf_num} position {pos_num} with "{held_album}".\n')
                        live_shelves[shelf_num][pos_num] = held_album
                        visited.add((shelf_num, pos_num))
                        break
                    else:
                        # The cycle continues
                        click.echo(f'Now holding "{held_album}".', nl=False)


    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == '__main__':
    sort_albums()
