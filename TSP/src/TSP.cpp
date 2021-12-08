#include "TSP.hpp"

#include <algorithm>
#include <stack>
#include <optional>
#include <map>
#include <climits>
#include <iterator>


std::ostream& operator<<(std::ostream& os, const CostMatrix& cm) {
    for (std::size_t r = 0; r < cm.size(); ++r) {
        for (std::size_t c = 0; c < cm.size(); ++c) {
            const auto& elem = cm[r][c];
            os << (is_inf(elem) ? "INF" : std::to_string(elem)) << " ";
        }
        os << "\n";
    }
    os << std::endl;

    return os;
}

/* PART 1 */

/**
 * Create path from unsorted path and last 2x2 cost matrix.
 * @return The vector of consecutive vertex.
 */
path_t StageState::get_path() {
    unsorted_path_t unsorted_path = StageState::get_unsorted_path();
    path_t sorted_path;

    NewVertex vertex_1;
    NewVertex vertex_2;

    std::vector<NewVertex> vertices = {vertex_1, vertex_2};

    for (auto &vertex : vertices){
        vertex = choose_new_vertex();
        reduce_cost_matrix();
        update_cost_matrix(vertex.coordinates);
    }

    for (auto &vertex : vertices){
        unsorted_path.push_back(vertex.coordinates);
    }

    std::size_t vertex = unsorted_path[0].col;

    sorted_path.push_back(vertex + 1);

    unsorted_path.erase(unsorted_path.begin());

    while (!unsorted_path.empty()){
        for (auto i = unsorted_path.begin(); i != unsorted_path.end(); ++i){
            if (i->row == vertex){
                vertex = i->col;
                sorted_path.push_back(vertex + 1);
                unsorted_path.erase(i);

                break;
            }
        }
    }

    return sorted_path;
}

/**
 * Get minimum values from each row and returns them.
 * @return Vector of minimum values in row.
 */
std::vector<cost_t> CostMatrix::get_min_values_in_rows() const {
    std::vector<cost_t> min_values = {};

    for (size_t i = 0; i < CostMatrix::size(); i++){
        min_values.push_back(*std::min_element(CostMatrix::get_matrix()[i].begin(), CostMatrix::get_matrix()[i].end()));
    }

    std::replace(min_values.begin(), min_values.end(), INF, 0);

    return min_values;
}

/**
 * Reduce rows so that in each row at least one zero value is present.
 * @return Sum of values reduced in rows.
 */
cost_t CostMatrix::reduce_rows() {
    std::vector<cost_t> min_values = CostMatrix::get_min_values_in_rows();

    for (size_t i = 0; i < CostMatrix::size(); i++){
        for (size_t j = 0; j < CostMatrix::size(); j++){
            if (CostMatrix::get_matrix()[i][j] == INF) { continue;}
            else { CostMatrix::matrix_[i][j] = CostMatrix::matrix_[i][j] - min_values[i]; }
        }
    }

    cost_t sum = std::accumulate(min_values.begin(), min_values.end(), 0);

    return sum;
}

/**
 * Get minimum values from each column and returns them.
 * @return Vector of minimum values in columns.
 */
std::vector<cost_t> CostMatrix::get_min_values_in_cols() const {
    std::vector<cost_t> min_values = {};

    for (size_t i = 0; i < CostMatrix::size(); i++) {
        std::vector<cost_t> column;

        for (size_t j = 0; j < CostMatrix::size(); j++) { column.push_back(CostMatrix::get_matrix()[j][i]); }

        min_values.push_back(*std::min_element(column.begin(), column.end()));
    }

    std::replace(min_values.begin(), min_values.end(), INF, 0);

    return min_values;
}

/**
 * Reduces rows so that in each column at least one zero value is present.
 * @return Sum of values reduced in columns.
 */
cost_t CostMatrix::reduce_cols() {
    std::vector<cost_t> min_values = CostMatrix::get_min_values_in_cols();

    for (std::size_t i = 0; i < CostMatrix::size(); i++){
        for (auto & j : CostMatrix::matrix_) { if (j[i] != INF){ j[i] = j[i] - min_values[i]; }
        }
    }

    cost_t sum = std::accumulate(min_values.begin(), min_values.end(), 0);

    return sum;
}

/**
 * Get the cost of not visiting the vertex_t (@see: get_new_vertex())
 * @param row
 * @param col
 * @return The sum of minimal values in row and col, excluding the intersection value.
 */
cost_t CostMatrix::get_vertex_cost(std::size_t row, std::size_t col) const {
    cost_t min_row_value = INF;
    cost_t min_col_value = INF;

    for (std::size_t i = 0; i < CostMatrix::size(); i++){
        if (i != row) { min_row_value = std::min(min_row_value, CostMatrix::get_matrix()[i][col]); }
    }

    for (std::size_t i = 0; i < CostMatrix::size(); i++){
        if (i != col) { min_col_value = std::min(min_col_value, CostMatrix::get_matrix()[row][i]); }
    }

    if (min_row_value == INF or min_col_value == INF) { return INF; }

    cost_t cost = min_row_value + min_col_value;

    return cost;
}

/* PART 2 */

/**
 * Choose next vertex to visit:
 * - Look for vertex_t (pair row and column) with value 0 in the current cost matrix.
 * - Get the vertex_t cost (calls get_vertex_cost()).
 * - Choose the vertex_t with maximum cost and returns it.
 * @param cm
 * @return The coordinates of the next vertex.
 */
NewVertex StageState::choose_new_vertex() {
    NewVertex new_vertex({}, -1);

    for (std::size_t i = 0; i < StageState::get_matrix().size(); i++){
        for (std::size_t j = 0; j < StageState::get_matrix().size(); j++){
            if (StageState::get_matrix()[i][j] == 0) {
                cost_t vertex_cost = StageState::get_matrix().get_vertex_cost(i, j);

                if (vertex_cost > new_vertex.cost){
                    new_vertex.cost = vertex_cost;
                    new_vertex.coordinates.row = i;
                    new_vertex.coordinates.col = j;
                }
            }
        }
    }

    return new_vertex;
}

/**
 * Update the cost matrix with the new vertex.
 * @param new_vertex
 */
void StageState::update_cost_matrix(vertex_t new_vertex) {
    std::size_t row = new_vertex.row;
    std::size_t col = new_vertex.col;

    for (std::size_t i = 0; i < StageState::get_matrix().size(); i++){
        StageState::matrix_[row][i] = INF;
        StageState::matrix_[i][col] = INF;
    }

    StageState::matrix_[col][row] = INF;
}

/**
 * Reduce the cost matrix.
 * @return The sum of reduced values.
 */
cost_t StageState::reduce_cost_matrix() {
    cost_t row_values = StageState::matrix_.reduce_rows();
    cost_t col_values = StageState::matrix_.reduce_cols();

    return row_values + col_values;
}


/**
 * Given the optimal path, return the optimal cost.
 * @param optimal_path
 * @param m
 * @return Cost of the path.
 */
cost_t get_optimal_cost(const path_t& optimal_path, const cost_matrix_t& m) {
    cost_t cost = 0;

    for (std::size_t idx = 1; idx < optimal_path.size(); ++idx) {
        cost += m[optimal_path[idx - 1] - 1][optimal_path[idx] - 1];
    }

    // Add the cost of returning from the last city to the initial one.
    cost += m[optimal_path[optimal_path.size() - 1] - 1][optimal_path[0] - 1];

    return cost;
}

/**
 * Create the right branch matrix with the chosen vertex forbidden and the new lower bound.
 * @param m
 * @param v
 * @param lb
 * @return New branch.
 */
StageState create_right_branch_matrix(cost_matrix_t m, vertex_t v, cost_t lb) {
    CostMatrix cm(m);
    cm[v.row][v.col] = INF;
    return StageState(cm, {}, lb);
}

/**
 * Retain only optimal ones (from all possible ones).
 * @param solutions
 * @return Vector of optimal solutions.
 */
tsp_solutions_t filter_solutions(tsp_solutions_t solutions) {
    cost_t optimal_cost = INF;
    for (const auto& s : solutions) {
        optimal_cost = (s.lower_bound < optimal_cost) ? s.lower_bound : optimal_cost;
    }

    tsp_solutions_t optimal_solutions;
    std::copy_if(solutions.begin(), solutions.end(),
                 std::back_inserter(optimal_solutions),
                 [&optimal_cost](const tsp_solution_t& s) { return s.lower_bound == optimal_cost; }
    );

    return optimal_solutions;
}

/**
 * Solve the TSP.
 * @param cm The cost matrix.
 * @return A list of optimal solutions.
 */
tsp_solutions_t solve_tsp(const cost_matrix_t& cm) {

    StageState left_branch(cm);

    // The branch & bound tree.
    std::stack<StageState> tree_lifo;

    // The number of levels determines the number of steps before obtaining
    // a 2x2 matrix.
    std::size_t n_levels = cm.size() - 2; // 2?

    tree_lifo.push(left_branch);   // Use the first cost matrix as the root.

    cost_t best_lb = INF;
    tsp_solutions_t solutions;

    while (!tree_lifo.empty()) {

        left_branch = tree_lifo.top();
        tree_lifo.pop();

        while (left_branch.get_level() != n_levels && left_branch.get_lower_bound() <= best_lb) {
            // Repeat until a 2x2 matrix is obtained or the lower bound is too high...

            if (left_branch.get_level() == 0) {
                left_branch.reset_lower_bound();
            }

            // 1. Reduce the matrix in rows and columns.
            cost_t new_cost = left_branch.reduce_cost_matrix();; // @TODO (KROK 1)

            // 2. Update the lower bound and check the break condition.
            left_branch.update_lower_bound(new_cost);
            if (left_branch.get_lower_bound() > best_lb) {
                break;
            }

            // 3. Get new vertex and the cost of not choosing it.
            NewVertex new_vertex = NewVertex(); // @TODO (KROK 2)
            new_vertex = left_branch.choose_new_vertex();

            // 4. @TODO Update the path - use append_to_path method.
            left_branch.append_to_path(new_vertex.coordinates);

            // 5. @TODO (KROK 3) Update the cost matrix of the left branch.
            left_branch.update_cost_matrix(new_vertex.coordinates);

            // 6. Update the right branch and push it to the LIFO.
            cost_t new_lower_bound = left_branch.get_lower_bound() + new_vertex.cost;
            tree_lifo.push(create_right_branch_matrix(cm, new_vertex.coordinates,
                                                      new_lower_bound));
        }

        if (left_branch.get_lower_bound() <= best_lb) {
            // If the new solution is at least as good as the previous one,
            // save its lower bound and its path.
            best_lb = left_branch.get_lower_bound();
            path_t new_path = left_branch.get_path();
            solutions.push_back({get_optimal_cost(new_path, cm), new_path});
        }
    }

    return filter_solutions(solutions); // Filter solutions to find only optimal ones.
}
